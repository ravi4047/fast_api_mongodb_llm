from typing import Dict, Any, List, Tuple, Optional
from pydantic import BaseModel, Field

# Define state model
class ConversationGraphState(BaseModel):
    user_id: str
    conversation_id: str
    current_message: str
    conversation_history: List[Dict[str, Any]]
    intent: Optional[str] = None
    entities: Dict[str, Any] = {}
    context: Dict[str, Any] = {}
    response: Optional[str] = None
    db_operations: List[Dict[str, Any]] = [] ## I don't think I will be doing this one.
    error: Optional[str] = None

    # https://claude.ai/chat/74a39efa-66d4-41a6-9240-38eea7937760 - This one is picked from here.
    token_usage: Dict[str, int] = Field(default_factory=lambda: {"prompt": 0, "completion": 0, "total": 0})

    # https://claude.ai/chat/74a39efa-66d4-41a6-9240-38eea7937760
    ## It recommends to use database here.

