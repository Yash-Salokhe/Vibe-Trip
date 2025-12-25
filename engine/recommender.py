import pandas as pd
from engine.vibe_scorer import calculate_vibe_score
from engine.geo_clusterer import cluster_pois_by_proximity
from engine.vibe_config import ALL_VIBES
from dotenv import load_dotenv

def calculate_cluster_quality(cluster_pois, selected_vibe_cols):
    if len(cluster_pois) == 0:
        return 0.0
    avg_popularity = cluster_pois['popularity_score'].mean()
    
    if selected_vibe_cols:
        avg_vibe = cluster_pois[selected_vibe_cols].mean().mean()
    else:
        avg_vibe = 0.0
    size_bonus = min(len(cluster_pois) / 5, 1.0) * 2.0      
    cluster_score = (
        0.5 * avg_popularity +
        0.4 * avg_vibe +
        0.1 * size_bonus
    )
    
    return cluster_score


def recommend_pois(
    df,
    city,
    selected_vibes,
    num_recommendations=15,
    distance_km=1.5,
    quality_threshold=3.0,
    verbose=True
):
    city_pois = df[df['city'] == city].copy()
    
    if len(city_pois) == 0:
        raise ValueError(f"No POIs found for city: {city}")
    city_pois = city_pois.dropna(subset=['lat', 'lon'])
    if not selected_vibes:
        raise ValueError("Must select at least one vibe")
    
    city_pois['vibe_alignment'] = city_pois[selected_vibes].mean(axis=1)

    city_pois = cluster_pois_by_proximity(
        city_pois,
        distance_km=distance_km,
        min_samples=2
    )
    selected_vibe_cols = [v for v in selected_vibes if v in city_pois.columns]
    cluster_scores = {}
    weak_clusters = set()
    
    for cluster_id in city_pois['cluster_id'].unique():
        cluster_pois_group = city_pois[city_pois['cluster_id'] == cluster_id]
        cluster_score = calculate_cluster_quality(cluster_pois_group, selected_vibe_cols)
        cluster_scores[cluster_id] = cluster_score
        if cluster_score < quality_threshold:
            weak_clusters.add(cluster_id)
    
    city_pois['cluster_score'] = city_pois['cluster_id'].map(cluster_scores)
    
    city_pois['final_score'] = (
        0.6 * city_pois['vibe_alignment'] +
        0.4 * city_pois['popularity_score']
    )
    city_pois['final_score'] = city_pois.apply(
        lambda row: row['final_score'] * 0.8
        if row['cluster_id'] in weak_clusters
        else row['final_score'],
        axis=1
    )
    recommendations = city_pois.nlargest(num_recommendations, 'final_score')

    output_cols = [
        'name',
        'attraction_type',
        'vibe_alignment',
        'popularity_score',
        'final_score',
        'cluster_id'
    ]
    
    recommendations = recommendations[output_cols].reset_index(drop=True)    
    return recommendations
