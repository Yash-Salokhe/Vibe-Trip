import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from dotenv import load_dotenv

def cluster_pois_by_proximity(pois_df, distance_km=1.5, min_samples=2):
    
    pois_df = pois_df.copy()
    if 'lat' not in pois_df.columns or 'lon' not in pois_df.columns:
        raise ValueError("DataFrame must have 'lat' and 'lon' columns")
    
    if len(pois_df) == 0:
        pois_df['cluster_id'] = []
        return pois_df

    coords = np.radians(pois_df[['lat', 'lon']].values)
    earth_radius_km = 6371  
    eps_radians = distance_km / earth_radius_km
    
    db = DBSCAN(
        eps=eps_radians,
        min_samples=min_samples,
        metric='haversine'
    )
    
    cluster_labels = db.fit_predict(coords)
    pois_df['cluster_id'] = cluster_labels
    
    return pois_df


def get_cluster_summary(pois_df):
    summary = []
    
    for cluster_id in sorted(pois_df['cluster_id'].unique()):
        cluster_pois = pois_df[pois_df['cluster_id'] == cluster_id]
        
        center_lat = cluster_pois['lat'].mean()
        center_lon = cluster_pois['lon'].mean()
        
        if len(cluster_pois) > 1:
            center_coords = np.radians(np.array([[center_lat, center_lon]]))
            poi_coords = np.radians(cluster_pois[['lat', 'lon']].values)
            
            from sklearn.metrics.pairwise import haversine_distances
            distances = haversine_distances(center_coords, poi_coords) * 6371  
            max_radius_km = distances.max()
        else:
            max_radius_km = 0.0
        
        summary.append({
            'cluster_id': cluster_id,
            'num_pois': len(cluster_pois),
            'center_lat': center_lat,
            'center_lon': center_lon,
            'radius_km': max_radius_km,
            'poi_names': ', '.join(cluster_pois['name'].head(5).tolist()) + ('...' if len(cluster_pois) > 5 else '')
        })
    
    return pd.DataFrame(summary)

