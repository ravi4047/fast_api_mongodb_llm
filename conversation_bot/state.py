
from typing import List, Dict, Any, Optional

class ConversationGraphState:
    uid: str
    conversation_id: str
    # current_message: str ## 👉 There will be no current message. There will be user_description. We are just helping the user
    # what they say

    user_description:str
    summary: str ## This is the long term memory.

    conversation_history: List[Dict[str, Any]]
    intent: Optional[str] = None
    entities: Dict[str, Any] = {}
    context: Dict[str, Any] = {}
    response: Optional[str] = None
    db_operations: List[Dict[str, Any]] = [] ## I don't think I will be doing this one.
    error: Optional[str] = None

    # https://claude.ai/chat/74a39efa-66d4-41a6-9240-38eea7937760 - This one is picked from here.

    ### Dude Ravi, it's a Pydantic model stuff
    # token_usage: Dict[str, int] = Field(default_factory=lambda: {"prompt": 0, "completion": 0, "total": 0})

    # https://claude.ai/chat/74a39efa-66d4-41a6-9240-38eea7937760
    ## It recommends to use database here.