from pydantic import BaseModel,Field,model_validator
from typing import Union,List
from datetime import timedelta, date
from enum import Enum

class Vibe(str, Enum):
    RELAXED = "relaxed"
    ADVENTURE = "adventure"
    CULTURE = "culture"
    NIGHTLIFE = "nightlife"
    NATURE = "nature"
    FOOD = "food"
 
class DateRange(BaseModel):
    start_date: date = Field(..., alias="startDate")
    end_date: date = Field(..., alias="endDate")
    duration_days: int | None = None

    @model_validator(mode="after")
    def compute_duration(self):
        if self.end_date < self.start_date:
            raise ValueError("endDate must be on or after startDate")

        self.duration_days = (self.end_date - self.start_date).days + 1
        return self

class TripRequest(BaseModel):
    location: str
    dates: DateRange
    vibes: List[Vibe]