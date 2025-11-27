# Set ai companion dto

from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Literal
from persona_cloning.enums_stuff import AvatarName

class AiCompanionDto(BaseModel):
    # name: str
    # age: int
    # personality_id: str

    # You could also enforce these validations in the AiCompanionDto class using Pydantic validators.
    # # This is an example of manual validation here:
    # if not ai_companion_dto.name or len(ai_companion_dto.name) > 50:
    #     response.status_code = 400  # Bad Request
    #     return {"error": "AI companion name is required and should not exceed 50 characters"}
    # if ai_companion_dto.age < 18:
    #     response.status_code = 400  # Bad Request
    #     return {"error": "AI companion age must be 18 or older"}

    # Let's validate the name which should not exceed 50 characters
    name: str = Field(..., max_length=50, description="Name of the AI companion, should not exceed 50 characters")

    # Age should be an integer and at least 18 and at most 120
    age: int = Field(..., ge=18, le=120, description="Age of the AI companion, must be between 18 and 120")

    # Personality ID should be a string and belongs to a predefined set of personalities i.e AvatarName enum
    personality: AvatarName = Field(..., description="Personality ID of the AI companion, must be one of the predefined AvatarName values")