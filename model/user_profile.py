from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId

# For match-making...
class UserProfile(BaseModel):
    """User profile model."""
    id: ObjectId = Field(alias="_id")
    name: str
    age: int
    gender: str
    bio: str
    interests: List[str]
    hobbies: List[str] ## I am adding this new one now
    photos: List[str]
    location: Dict[str, float]  # {"lat": 40.7128, "lng": -74.0060}
    preferences: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}