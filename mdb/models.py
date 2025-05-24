from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr, ConfigDict

# MongoDB Collections:
USERS_COLLECTION = "users"
CONVERSATIONS_COLLECTION = "conversations"
MESSAGES_COLLECTION = "messages"
MATCHES_COLLECTION = "matches"
TASKS_COLLECTION = "tasks"

# Base MongoDB document model
class MongoBaseModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # class Config:
    #     populate_by_name = True
    #     arbitrary_types_allowed = True

    model_config = ConfigDict(
        # populate_by_name=True, ## It's deprecated. 
        ### These two are same as populate_by_name=True
        validate_by_name=True,
        validate_by_alias=True,

        arbitrary_types_allowed=True
    )

# User-related models
class UserProfile(MongoBaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    first_name: str
    last_name: str
    birth_date: datetime
    gender: str
    interests: List[str] = []
    bio: Optional[str] = None
    location: Optional[Dict[str, float]] = None  # {"lat": 40.7128, "lng": -74.0060}
    profile_picture_url: Optional[str] = None
    is_active: bool = True
    last_active: datetime = Field(default_factory=datetime.utcnow)
    preferences: Dict[str, Any] = {}

class Match(MongoBaseModel):
    user_id_1: str
    user_id_2: str
    match_date: datetime = Field(default_factory=datetime.utcnow)
    status: str = "active"  # active, paused, ended
    compatibility_score: Optional[float] = None

class Message(MongoBaseModel):
    sender_id: str
    receiver_id: str
    content: str
    read: bool = False
    read_at: Optional[datetime] = None

class Conversation(MongoBaseModel):
    user_id_1: str
    user_id_2: str
    last_message_id: Optional[str] = None
    last_message_at: Optional[datetime] = None
    messages_count: int = 0
    is_active: bool = True

class UserTask(MongoBaseModel):
    user_id: str
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    is_completed: bool = False
    completed_at: Optional[datetime] = None
    priority: str = "medium"  # low, medium, high
    tags: List[str] = []

# AI Conversation models
class ConversationState(MongoBaseModel):
    user_id: str
    conversation_id: str
    current_intent: Optional[str] = None
    entities: Dict[str, Any] = {}
    conversation_history: List[Dict[str, Any]] = []
    last_response: Optional[str] = None
    context: Dict[str, Any] = {}