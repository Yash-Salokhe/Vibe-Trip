ACTUAL_ATTRACTION_TYPES = [
    'attraction', 'unknown', 'pub', 'gate', 'restaurant', 'information',
    'museum', 'zoo', 'castle', 'monument', 'memorial', 'gallery', 'bar',
    'park', 'beach', 'theatre', 'artwork', 'hotel', 'apartment', 'cave',
    'resort', 'trail', 'aquarium', 'archaeological_site', 'cafe',
    'waterfall', 'guest_house', 'nature_reserve', 'nightclub', 'hostel'
]

VIBE_TYPE_MAPPING = {
    'vibe_historic_cultural': [
        'monument',              
        'memorial',              
        'castle',                
        'archaeological_site',   
        'gate',                  
        'museum',               
    ],
    
    'vibe_nature_outdoors': [
        'park',                  
        'trail',                 
        'nature_reserve',        
        'waterfall',             
        'beach',                 
        'zoo',                   
        'aquarium',              
        'cave',                  
    ],
    
    'vibe_art_architecture': [
        'gallery',               
        'artwork',               
        'museum',                
        'theatre',               
    ],
    
    'vibe_nightlife_entertainment': [
        'bar',                   
        'nightclub',             
        'pub',                   
        'theatre',               
        'restaurant',            
    ],
    
    'vibe_food_wine': [
        'restaurant',            
        'cafe',                  
        'pub',                   
        'bar',                   
    ],
    
    'vibe_adventure_activities': [
        'trail',                 
        'cave',                  
        'aquarium',              
        'zoo',                   
        'beach',                 
        'waterfall',             
    ],
    
    'vibe_urban_exploration': [
        'park',                  
        'monument',              
        'gallery',               
        'museum',                
        'bar',                   
        'restaurant',            
        'cafe',                  
        'gate',                  
    ],
    
    'vibe_beach_relaxation': [
        'beach',                 
        'resort',                
        'cafe',                  
    ],
}

VIBE_CATEGORY_KEYWORDS = {
    'vibe_historic_cultural': [
        'historic', 'cultural', 'heritage', 'historical', 'ancient',
        'preserved', 'medieval', 'monument', 'artifact'
    ],
    'vibe_nature_outdoors': [
        'nature', 'outdoor', 'natural', 'park', 'forest', 'mountain',
        'scenic', 'wildlife', 'garden', 'botanical'
    ],
    'vibe_art_architecture': [
        'art', 'architecture', 'gallery', 'museum', 'painting',
        'sculpture', 'design', 'installation'
    ],
    'vibe_nightlife_entertainment': [
        'nightlife', 'entertainment', 'bar', 'club', 'nightclub',
        'dance', 'live', 'music', 'performance'
    ],
    'vibe_food_wine': [
        'food', 'restaurant', 'cuisine', 'wine', 'cafe', 'dining',
        'culinary', 'tavern', 'bistro'
    ],
    'vibe_adventure_activities': [
        'adventure', 'activity', 'hiking', 'climbing', 'water',
        'extreme', 'outdoor', 'sport', 'active'
    ],
    'vibe_urban_exploration': [
        'urban', 'city', 'street', 'neighborhood', 'district',
        'street art', 'market', 'plaza', 'square'
    ],
    'vibe_beach_relaxation': [
        'beach', 'sand', 'sea', 'coast', 'relax', 'resort',
        'tropical', 'island'
    ],
}


VIBE_DESCRIPTION_KEYWORDS = {
    'vibe_historic_cultural': [
        'historic', 'ancient', 'historical', 'preserved', 'century',
        'medieval', 'traditional', 'heritage'
    ],
    'vibe_nature_outdoors': [
        'forest', 'mountain', 'scenic', 'wildlife', 'garden',
        'botanical', 'natural', 'outdoor', 'nature'
    ],
    'vibe_art_architecture': [
        'art', 'painting', 'sculpture', 'architecture',
        'design', 'creative', 'artistic'
    ],
    'vibe_nightlife_entertainment': [
        'nightlife', 'entertainment', 'dance', 'live', 'music',
        'performance', 'night', 'party'
    ],
    'vibe_food_wine': [
        'restaurant', 'cuisine', 'wine', 'food', 'dining',
        'culinary', 'chef'
    ],
    'vibe_adventure_activities': [
        'adventure', 'hiking', 'climbing', 'water', 'extreme',
        'sport', 'active', 'thrilling'
    ],
    'vibe_urban_exploration': [
        'street', 'district', 'neighborhood', 'urban', 'city',
        'market', 'plaza', 'square', 'alley'
    ],
    'vibe_beach_relaxation': [
        'beach', 'sand', 'sea', 'coast', 'relax', 'tropical',
        'island', 'swim'
    ],
}

VIBE_WEIGHTS = {
    'description_match': 3.0,    
    'type_match': 1.5,           
    'category_match': 0.5,       
}

MAX_VIBE_SCORE = 5.0

VIBE_DESCRIPTIONS = {
    'vibe_historic_cultural': 'Monuments, museums, historical sites & cultural heritage',
    'vibe_nature_outdoors': 'Parks, hiking, wildlife & natural landscapes',
    'vibe_art_architecture': 'Galleries, museums, architecture & artistic spaces',
    'vibe_nightlife_entertainment': 'Bars, clubs, live music & evening entertainment',
    'vibe_food_wine': 'Restaurants, cafes, dining & culinary experiences',
    'vibe_adventure_activities': 'Hiking, water sports, caves & active pursuits',
    'vibe_urban_exploration': 'City streets, landmarks, neighborhoods & street life',
    'vibe_beach_relaxation': 'Beaches, resorts & coastal relaxation',
}
ALL_VIBES = list(VIBE_TYPE_MAPPING.keys())
