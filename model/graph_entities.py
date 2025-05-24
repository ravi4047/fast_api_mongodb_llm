from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

# Intent recognition schema
class IntentRecognitionResult(BaseModel):
    intent: str = Field(description="The detected intent of the user message")
    confidence: float = Field(description="Confidence score between 0 and 1")
    
    class Config:
        schema_extra = {
            "examples": [
                {
                    "intent": "profile_info_request",
                    "confidence": 0.92
                }
            ]
        }

# Entity extraction schema
class Entity(BaseModel):
    name: str = Field(description="Name of the extracted entity")
    value: str = Field(description="Value of the extracted entity")
    type: str = Field(description="Type of entity (user, date, location, etc.)")

class EntityExtractionResult(BaseModel):
    entities: List[Entity] = Field(description="List of extracted entities")


## -----------------------------------------------------------------------------------------------------------

# Schema for profile information requests
class ProfileInfoRequest(BaseModel):
    target_user_id: str = Field(description="ID of the user whose profile information is requested")
    requested_fields: List[str] = Field(description="Fields of profile information requested")
    
    class Config:
        schema_extra = {
            "examples": [
                {
                    "target_user_id": "user123",
                    "requested_fields": ["birthday", "interests", "location"]
                }
            ]
        }

# Schema for message information requests
class MessageInfoRequest(BaseModel):
    conversation_id: Optional[str] = Field(None, description="ID of the specific conversation")
    target_user_id: Optional[str] = Field(None, description="ID of the user whose messages are requested")
    time_range: Optional[Dict[str, datetime]] = Field(None, description="Time range for message filtering")
    limit: int = Field(10, description="Maximum number of messages to retrieve")
    
    class Config:
        schema_extra = {
            "examples": [
                {
                    "target_user_id": "user123",
                    "limit": 5
                }
            ]
        }

# Schema for match information requests
class MatchInfoRequest(BaseModel):
    match_status: Optional[str] = Field(None, description="Status of matches to retrieve (new, active, all)")
    limit: int = Field(10, description="Maximum number of matches to retrieve")
    sort_by: Optional[str] = Field(None, description="Field to sort matches by")
    
    class Config:
        schema_extra = {
            "examples": [
                {
                    "match_status": "new",
                    "limit": 5,
                    "sort_by": "created_at"
                }
            ]
        }