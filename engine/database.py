import os
import pandas as pd
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "vibetrip"
COLLECTION_NAME = "Global_Pois"
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

async def get_all_cities():
    try:
        cities = await collection.distinct("city")
        return sorted([city for city in cities if city])
    except Exception as e:
        print(f"Database Error (get_all_cities): {e}")
        return []

async def get_city_pois(city_name: str):
    try:
        cursor = collection.find({"city": city_name})
        results = await cursor.to_list(length=2000) 
        
        if not results:
            return pd.DataFrame()
        
        df = pd.DataFrame(results)
        if '_id' in df.columns:
            df = df.drop(columns=['_id'])
            
        return df
    except Exception as e:
        print(f"Database Error (get_city_pois): {e}")
        return pd.DataFrame()

async def check_connection():
    try:
        await client.admin.command('ping')
        return True
    except Exception:
        return False