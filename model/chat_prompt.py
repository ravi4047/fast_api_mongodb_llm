from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId
from typing import Optional

## I am planning to use the ChatPrompt or the DialogPrompt to save both user prompt and the ai content.
class ChatPrompt(BaseModel):
    """ChatPrompt model."""
    # id: Optional[str] = Field(alias="_id")
    id: Optional[ObjectId] = Field(alias="_id")
    conversation_id: str
    user_prompt: str
    ai_content: str
    timestamp: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    # @staticmethod
    # def create_object()->ChatPrompt:

    # Copilot helped me to create a method so that I can create the object here only
    @classmethod
    def create(cls, conv_id: str, user_prompt:str, ai_content:str, timestamp: datetime):
        """Create and return a new ChatPrompt instance"""
        return cls(_id=ObjectId(), conversation_id=conv_id, user_prompt=user_prompt, ai_content=ai_content, timestamp=timestamp)
    

class Conversation(BaseModel):
    """Conversation model"""
    # id: Optional[str] = Field(...,alias="_id")
    id: Optional[ObjectId] = Field(...,alias="_id")
    title: str
    uid: str
    timestamp: datetime
    long_term_memory: str ## This is for conversation.

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    @classmethod
    def create(cls, title:str, uid:str, timestamp: datetime):
        """Create and return a new ChatPrompt instance"""
        return cls(_id=ObjectId(), title=title, uid=uid, timestamp=timestamp, long_term_memory="")

# 🤔🤔 When I try to import I only want ChatPrompt class to be exported not those which I have imported like BaseModel or datetime.
#  How to make it private in fastapi

#✅ Solution in copilot: 

# Define __all__ to explicitly expose only ChatPrompt
__all__ = ["ChatPrompt"]


# By adding __all__, when someone imports using from module_name import *, only ChatPrompt will be accessible while BaseModel 
# and datetime remain private within the module.