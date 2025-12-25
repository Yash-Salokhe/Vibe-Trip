import pandas as pd
from engine.vibe_config import (
    VIBE_TYPE_MAPPING,
    VIBE_CATEGORY_KEYWORDS,
    VIBE_DESCRIPTION_KEYWORDS,
    VIBE_WEIGHTS,
    MAX_VIBE_SCORE,
    ALL_VIBES
)


def calculate_vibe_score(row, vibe):
    score = 0.0

    description_str = str(row['short_description']).lower()    
    for keyword in VIBE_DESCRIPTION_KEYWORDS[vibe]:
        if keyword in description_str:
            score += VIBE_WEIGHTS['description_match']  
    

    attraction_type = str(row['attraction_type']).lower().strip()    
    if attraction_type in VIBE_TYPE_MAPPING[vibe]:
        score += VIBE_WEIGHTS['type_match']  
    
    
    categories_str = str(row['categories']).lower()
    for keyword in VIBE_CATEGORY_KEYWORDS[vibe]:
        if keyword in categories_str:
            score += VIBE_WEIGHTS['category_match']  
    normalized_score = min(score, MAX_VIBE_SCORE)
    return normalized_score


def add_vibe_scores(df):
    df_copy = df.copy()
    
    for vibe in ALL_VIBES:
        df_copy[vibe] = df_copy.apply(
            lambda row: calculate_vibe_score(row, vibe),
            axis=1
        )
    
    return df_copy
