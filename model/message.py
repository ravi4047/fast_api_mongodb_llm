from pydantic import BaseModel, Field
from datetime import datetime


## It's related to AI as a messenger.
class Message(BaseModel):
    """Message model."""
    id: str = Field(alias="_id")
    from_user_id: str
    to_user_id: str
    content: str
    timestamp: datetime
    status: str  # "sent", "delivered", "read"