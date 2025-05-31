from fastapi import APIRouter, Request, Response
from typing import TypedDict

router = APIRouter()

class ChatRequest(TypedDict):
    uid: str
    message: str

class Conversation(TypedDict):
    

# === In-memory store for now ===
user_db = {}

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