# Persona response chat model
from typing import TypedDict, List

class PersonaChatResponse(TypedDict):
    id: str # Chat id
    user_message: str
    ai_response: str
    timestamp: str
    # session_number: int
    conversation_id: str

class PersonaConnectWsResponse(TypedDict):
    user_id: str
    conversation_id: str
    connection_id: str

class SetAiCompanionResponse(TypedDict):
    # ai_companion: 'AiCompanionDto'  # Forward reference to AiCompanionDto
    conversation_id: str