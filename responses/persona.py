# Persona response chat model
from typing import TypedDict, List

class PersonaChatResponse(TypedDict):
    user_message: str
    ai_response: str
    timestamp: str
    session_number: int
    conversation_id: str

