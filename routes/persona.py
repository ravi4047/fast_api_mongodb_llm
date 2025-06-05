from fastapi import APIRouter, Request, Response
from typing import TypedDict

from responses.persona import PersonaChatResponse

router = APIRouter()

class ChatRequest(TypedDict):
    uid: str
    message: str

class Conversation(TypedDict):


# === In-memory store for now ===
user_db = {}

# 
@router.get("/", response_description="List all conversations", response_model=list[Conversation])
async def chat_with_ai(request: Request, req: ChatRequest): #(dto: PagingRequestDto):
    original_message = req.message
    user_id = req.user_id

    lang = detect(original_message)
    translated_input = translator.translate(original_message, src=lang, dest="en").text

    bot_response = generate_response(translated_input)
    translated_bot = translator.translate(bot_response, src="en", dest=lang).text

    # Analyze behavior
    emotion, tone, love_language = analyze_emotion(translated_input)

    # Store it (in memory for now)
    chat_entry = {
        "user_message": original_message,
        "bot_response": translated_bot,
        "emotion": emotion,
        "tone": tone,
        "love_language": love_language
    }

    user_db.setdefault(user_id, []).append(chat_entry)

    return {
        "bot_response": translated_bot,
        "detected_language": lang,
        "emotion": emotion,
        "tone": tone,
        "love_language": love_language
    }

## Connect the websocket.

@router.post("/", response_description="Create a new persona chat", response_model=PersonaChatResponse)
async def create_persona_chat(request: Request, chatRequest: ChatRequest, response: Response, req: ChatRequest):
    user_id = request.headers.get("uid") 
    if not user_id:
        response.status_code = 400 # Bad Request
        return {"error": "User ID is required"}
    
    message = chatRequest.get("message")
    if not message:
        response.status_code = 400 # Bad Request
        return {"error": "Message is required"}
    
    # https://claude.ai/chat/c5d85244-f76c-4e20-ab60-eab33b9d9ca5
    # This Claude link gave me the best advice.

    # Let's make it stateless

    # First, get the 
    
    # Process the message and generate a response

    # Here you would typically call your service layer to handle the business logic
    # For now, we'll just echo the message back
    response_data = PersonaChatResponse(
        user_message=message,
        ai_response="This is a mock AI response",
        timestamp="2023-01-01T00:00:00Z",
        session_number=1,
        conversation_id="conv_123"
    )

    return response_data

