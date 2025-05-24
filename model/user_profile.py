from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# For match-making...
class UserProfile(BaseModel):
    """User profile model."""
    id: str = Field(alias="_id")
    name: str
    age: int
    gender: str
    bio: str
    interests: List[str]
    photos: List[str]
    location: Dict[str, float]  # {"lat": 40.7128, "lng": -74.0060}
    preferences: Dict[str, Any]
    created_at: datetime
    updated_at: datetime