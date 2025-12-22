from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Union,List
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/",response_class=HTMLResponse)
async def index(request: Request): 
    return templates.TemplateResponse(
        "index.html", {"request": request}
    )

@app.get("/itinerary", response_class=HTMLResponse)
async def get_itinerary_page(request: Request):
    print("in the itinerary")
    return templates.TemplateResponse("itinerary.html", {"request": request})

@app.post("/api/generate")
async def generate_itinerary(data: dict):
    location = data.get("location")
    vibes = data.get("vibes")
    days = data.get("days")
    print(data)
    # This is where you'd call your model logic
    # result = model.generate(location, vibes, days)
    
    return {
        "itinerary": f"Successfully generated a {days}-day plan for {location}!",
        "pois": ["Eiffel Tower", "Louvre Museum"] # Example data
    }