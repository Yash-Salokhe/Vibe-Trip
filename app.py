import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from langchain_core.messages import HumanMessage, AIMessage
from engine.database import get_city_pois, get_all_cities
from engine.recommender import recommend_pois
from engine.itinerary_builder import generate_itinerary 

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request): 
    cities = await get_all_cities()
    return templates.TemplateResponse(
        "index.html", {"request": request, "cities": cities}
    )

@app.get("/itinerary", response_class=HTMLResponse)
async def get_itinerary_page(request: Request):
    return templates.TemplateResponse("itinerary.html", {"request": request})

@app.post("/api/generate")
async def generate_itinerary_api(data: dict):
    location = data.get("location")
    vibes = data.get("vibes", [])
    days = data.get("days", 3)
    raw_history = data.get("history", [])

    user_input = "Please generate a full itinerary."
    if raw_history:
        user_input = raw_history[-1].get("content", user_input)
    formatted_history = []
    for msg in raw_history[:-1]:
        if msg['role'] == 'user':
            formatted_history.append(HumanMessage(content=msg['content']))
        else:
            formatted_history.append(AIMessage(content=msg['content']))

    city_df = await get_city_pois(location)
    if city_df.empty:
        return {"error": f"No data found for {location}"}

    recommendations_df = recommend_pois(
        df=city_df,
        city=location,
        selected_vibes=vibes,
        num_recommendations=15 
    )
    try:
        itinerary_json = await generate_itinerary(
            location=location,
            days=days,
            poi_df=recommendations_df,
            history=formatted_history,
            user_input=user_input
        )
        
        return {
            "structured_itinerary": itinerary_json.get('itinerary', []),
            "travel_tips": itinerary_json.get('travel_tips', ""),
            "raw_pois": recommendations_df.to_dict(orient='records') 
        }
        
    except Exception as e:
        print(f"LLM Error: {e}")
        return {
            "error": "LLM failed to generate narrative.",
            "raw_pois": recommendations_df.to_dict(orient='records')
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)