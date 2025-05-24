# https://claude.ai/chat/3189db2e-a00b-489b-8118-b1a5d97f8dc5
from pydantic import BaseModel
from datetime import datetime

class FeedHistoryEntry(BaseModel):
    """Entry in feed history."""
    user_id: str
    profile_id: str
    timestamp: datetime