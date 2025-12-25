import pandas as pd
import numpy as np
from xgboost import XGBRanker
import pickle
from dotenv import loadenv
from engine.vibe_scorer import add_vibe_scores, calculate_vibe_score
from engine.geo_clusterer import cluster_pois_by_proximity
from engine.vibe_config import ALL_VIBES, VIBE_DESCRIPTIONS


class VibeTriPRecommender:

    def __init__(self, model_path='ranking_model.json', pois_path='global_pois_wikidata.csv'):        
        self.model = XGBRanker()
        self.model.load_model(model_path)

        self.feature_cols = [
            'vibe_alignment',
            'popularity_score',
            'cluster_size',
            'popularity_rank',
            'vibe_popularity_ratio',
            'is_isolated',
            'vibe_aligned',
            'article_length_normalized',
            'references_normalized',
            'must_see_flag',
            'recency_signal',
            'is_outdoor',
            'unesco'
        ]
        self.df = pd.read_csv(pois_path)
        self.df = add_vibe_scores(self.df)
    
    def engineer_inference_features(self, city_pois):
        df = city_pois.copy()
        
        df['num_references'] = df['num_references'].fillna(0)
        df['article_length'] = df['article_length'].fillna(0)
        df['must_see_flag'] = df['must_see_flag'].fillna(0)
        df['is_outdoor'] = df['is_outdoor'].fillna(0)
        df['pageviews_30d'] = df['pageviews_30d'].fillna(0)
        df['pageviews_365d'] = df['pageviews_365d'].fillna(1)
        df['unesco'] = df['unesco'].fillna(0)
        
        cluster_counts = df.groupby('cluster_id').size().reset_index(name='cluster_size')
        df = df.merge(cluster_counts, on='cluster_id', how='left')
        df['cluster_size'] = df['cluster_size'].fillna(1)
        
        df['popularity_rank'] = df['popularity_score'].rank(pct=True)
        
        df['vibe_popularity_ratio'] = (
            df['vibe_alignment'] / (df['popularity_score'] + 1)
        )
        
        df['is_isolated'] = (df['cluster_id'] == -1).astype(int)

        df['vibe_aligned'] = df['vibe_alignment'] / 5.0
        
        max_article_length = df['article_length'].max()
        if max_article_length > 0:
            df['article_length_normalized'] = df['article_length'] / max_article_length
        else:
            df['article_length_normalized'] = 0

        max_references = df['num_references'].max()
        if max_references > 0:
            df['references_normalized'] = df['num_references'] / max_references
        else:
            df['references_normalized'] = 0

        df['recency_signal'] = (
            df['pageviews_30d'] / (df['pageviews_365d'] + 1)
        )
        
        return df
    
    def recommend(self, city, selected_vibes, num_recommendations=15, distance_km=1.5):
        city_pois = self.df[self.df['city'] == city].copy()
        city_pois = city_pois.dropna(subset=['lat', 'lon'])
        
        if len(city_pois) == 0:
            raise ValueError(f"No POIs found for city: {city}")

        city_pois['vibe_alignment'] = 0.0
        
        for vibe in selected_vibes:
            if vibe not in city_pois.columns:
                city_pois[vibe] = city_pois.apply(
                    lambda row: calculate_vibe_score(row, vibe),
                    axis=1
                )
            city_pois['vibe_alignment'] += city_pois[vibe]
        
        city_pois['vibe_alignment'] /= len(selected_vibes)        
        city_pois = cluster_pois_by_proximity(city_pois, distance_km=distance_km, min_samples=2)

        city_pois = self.engineer_inference_features(city_pois)
        X = city_pois[self.feature_cols].values
        
        model_scores = self.model.predict(X)
        city_pois['model_score'] = model_scores
        
        city_pois['final_score'] = (
            0.6 * city_pois['vibe_alignment'] +
            0.2 * city_pois['popularity_score'] +
            0.2 * city_pois['model_score']
        )
        
        recommendations = city_pois.nlargest(num_recommendations, 'final_score')

        output_cols = [
            'name',
            'attraction_type',
            'vibe_alignment',
            'popularity_score',
            'model_score',
            'final_score',
            'cluster_id',
            'short_description'
        ]
        
        recommendations = recommendations[output_cols].reset_index(drop=True)      
        return recommendations
    
    def display_recommendations(self, recommendations, num_to_show=10):
        print(f"\n{'='*70}")
        print(f"TOP {min(num_to_show, len(recommendations))} RECOMMENDATIONS")
        print(f"{'='*70}\n")
        
        for idx, row in recommendations.head(num_to_show).iterrows():
            print(f"{idx+1}. {row['name']}")
            print(f"   Type: {row['attraction_type']}")
            print(f"   Vibe Match: {row['vibe_alignment']:.2f}/5.0 | Popularity: {row['popularity_score']:.2f}")
            print(f"   Final Score: {row['final_score']:.2f}")
            print(f"   Description: {row['short_description'][:100]}...")
            print()

