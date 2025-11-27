from datetime import datetime
from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel

# from responses.persona import PersonaChatResponse

from dto.persona import AiCompanionDto
from model.chat_prompt import Conversation
from persona_cloning.config.personality import get_personality_by_name
from persona_cloning.models.persona import PersonaScore, PersonaScores
from persona_cloning.models.store import conv_store_manager
from persona_cloning.persona_clone_ai_partner import PersonaCloneAIPartner
from response_me.persona import PersonaChatResponse, SetAiCompanionResponse

router = APIRouter()

from main import mdb_manager

class PostChatRequestDto(BaseModel):
    uid: str
    message: str
    connection_id: str

class ConnectRequestDto(BaseModel):
    user_id: str
    conversation_id: str
    connection_id: str


# === In-memory store for now ===
# user_db = {}

# @router.get("/", response_description="List all conversations", response_model=list[Conversation])
# async def chat_with_ai(request: Request): #(dto: PagingRequestDto):
#     original_message = req.message
#     user_id = req.user_id

#     lang = detect(original_message)
#     translated_input = translator.translate(original_message, src=lang, dest="en").text

#     bot_response = generate_response(translated_input)
#     translated_bot = translator.translate(bot_response, src="en", dest=lang).text

#     # Analyze behavior
#     emotion, tone, love_language = analyze_emotion(translated_input)

#     # Store it (in memory for now)
#     chat_entry = {
#         "user_message": original_message,
#         "bot_response": translated_bot,
#         "emotion": emotion,
#         "tone": tone,
#         "love_language": love_language
#     }

#     user_db.setdefault(user_id, []).append(chat_entry)

#     return {
#         "bot_response": translated_bot,
#         "detected_language": lang,
#         "emotion": emotion,
#         "tone": tone,
#         "love_language": love_language
#     }

## Connect the websocket
## I don't this AWS websocket works with FastAPI, so we will use the HTTP POST method for now -- start
# @router.websocket("/ws/{user_id}/{conversation_id}/{connection_id}")
# async def websocket_endpoint(websocket, user_id: str, conversation_id: str, connection_id: str):
#     await websocket.accept()
#     # Here you would typically fetch or create a conversation store for the user
#     conv_store = conv_store_manager.get_store(user_id, conversation_id, connection_id)

#     try:
#         while True:
#             data = await websocket.receive_text()
#             # Process the incoming message and generate a response
#             ai_response = "This is a mock AI response"  # Placeholder for AI response generation logic
            
#             # Add the chat to the conversation store
#             conv_store.add_chat(
#                 message=data,
#                 timestamp=datetime.now()
#             )

#             await websocket.send_text(ai_response)
#     except Exception as e:
#         print(f"WebSocket error: {e}")
#         await websocket.close()
# -- stop

# Connect a new persona chat session
@router.post("/connect", response_description="Connect a new persona chat session", response_model=ConnectRequestDto)
async def connect_persona_chat(request: Request, connectRequest: ConnectRequestDto, response: Response):
    user_id = request.headers.get("uid") 
    if not user_id:
        response.status_code = 400 # Bad Request
        return {"error": "User ID is required"}
    
    # Validate the connectRequest body
    if not connectRequest.conversation_id or not connectRequest.connection_id:
        response.status_code = 400 # Bad Request
        return {"error": "Conversation ID and Connection ID are required"}

    try:
        # Fetch the user profile from the database
        user_profile = await mdb_manager.get_user_profile(user_id)

        conv = await mdb_manager.get_conversation(connectRequest.conversation_id)
        
        conv_store_manager.set_conversation_store(
            user_profile=user_profile,
            conversation_id=connectRequest.conversation_id,
            connection_id=connectRequest.connection_id,
            ai_companion=conv.companion
        )

    except HTTPException as http_exc:
        response.status_code = http_exc.status_code
        return {"error": http_exc.detail}
    except Exception as e:
        response.status_code = 500
        return {"error": str(e)}
    
# Disconnect a persona chat session
@router.delete("/", response_description="Disconnect a persona chat session")
async def disconnect_persona_chat(request: Request, response: Response):
    user_id = request.headers.get("uid") 
    if not user_id:
        response.status_code = 400
        return {"error": "User ID is required"}

    connection_id = request.headers.get("connection_id")
    if not connection_id:
        response.status_code = 400
        return {"error": "Connection ID is required"}

    conv_store_manager.clear_store(connection_id)
    return {"message": "Disconnected successfully"}

# Post a message to the AI companion and get a response
# This is a stateless HTTP POST route to send a message to the AI companion and get a response
# The problem is that user can send multiple chats. Like the human way, they can chat regularly without 
# waiting for the ai response.
# But why do I care? No, I should.
# 👉👉 So technically, on every chat, it will process the chat and only return the response when no new chat is received.
@router.post("/chat", response_description="Receive a message and respond", response_model=PersonaChatResponse)
async def post_message(request: Request, chatRequest: PostChatRequestDto, response: Response):
    user_id = request.headers.get("uid") 
    try:
        if not user_id:
            response.status_code = 400 # Bad Request
            return {"error": "User ID is required"}
        
        # Validate the chatRequest body
        if not chatRequest.message:
            response.status_code = 400 # Bad Request
            return {"error": "Message is required"}
        
        # Here you would typically call your service layer to handle the business logic


        # Step 1. First save the chat message to the conversation in mongodb/dynamodb.
        # Reason, I will be saving the both  AI response in the same conversation and both chat messages only 
        # when the user chat is on the conversation.
        # 👉 If not there, then I won't save the AI response. That means, that's a waste processing.
        # It's just resembling the human way of chatting. We process every chat message and only return the response when 
        # the user has ended speaking from their side.

        # 👉 You are thinking right ravi? But the thing is AI will be always responsive unlike the human way.
        # So, we can just make it human turn and ai turn always.



        # Source: https://chatgpt.com/c/6843723f-29bc-800d-b755-3a7f81430317
#         {
#   "user_id": "123",
#   "chat_id": "abc",
#   "timestamp": "2024-06-07T12:34:56Z",
#   "sender": "ai",
#   "message": "Hello! How can I help you?",
#   "emotions": {
#     "joy": 0.8,
#     "sadness": 0.1
#   },
#   "metadata": {
#     "context_id": "xyz",
#     "message_type": "text"
#   }
# }
        timestamp = datetime.now()  # Use ISO format for timestamp

        mdb_manager.transact_user_chat() # Will save both in the chat and conversation collections
        # [update] No, not in conversation collection, but in the chat collection
        # Because we will be always last responding to the user, and on some rare cases, it's not required
        # for the AI response, then we will save to the conversation collection also.
        # 👉👉 [double update] Not, in chat collection, but in the conversation collection.

        # For now, instead of calling from database, we fetch from the in-memory store
        conv_store = conv_store_manager.get_store(chatRequest.connection_id)

        conv_store.add_recent_chat(message=chatRequest.message, timestamp=timestamp, is_ai=False)

        chat_history = conv_store
        emotion, tone, love_language = conv_store.analyze_emotion(chatRequest.message)
        
        # personality = get_personality_by_name(conv_store.ai_companion.personality) # This is not needed as we need the ai_companion from the conversation store

        persona_handler = PersonaCloneAIPartner(
            user_profile=conv_store.user_profile,
            ai_companion=conv_store.ai_companion,
            conversation_id=chatRequest.connection_id,
            persona_scores=PersonaScores()  # Assuming PersonaScores is a class that calculates scores based on the conversation
        )

        # Generate a response using the persona handler
        persona = await persona_handler.generate_response(chatRequest.message)

        # Add the chat response to the chat in dynamodb

        return PersonaChatResponse(
            id=chatRequest.connection_id,  # Assuming connection_id is used as the chat ID
            user_message=chatRequest.message,
            ai_response=persona.content.__str__(),  # This should call the AI response generation logic
            timestamp=datetime.now().isoformat(),  # Use ISO format for timestamp
            conversation_id=chatRequest.connection_id  # Assuming connection_id is used as the conversation ID
        )
    except Exception as e:
        response.status_code = 500
        return {"error": str(e)}

# --------- start
# @router.post("/", response_description="Connect a new persona chat session", response_model=PersonaChatResponse)
# async def create_persona_chat(request: Request, connectRequest: ConnectRequestDto, response: Response):
#     user_id = request.headers.get("uid") 
#     if not user_id:
#         response.status_code = 400 # Bad Request
#         return {"error": "User ID is required"}
    
#     ## I think BaseModel will handle the chatRequest body parsing
#     # message = chatRequest.get("message")
#     # if not message:
#     #     response.status_code = 400 # Bad Request
#     #     return {"error": "Message is required"}
    
#     # https://claude.ai/chat/c5d85244-f76c-4e20-ab60-eab33b9d9ca5
#     # This Claude link gave me the best advice

#     # Let's make it stateless

#     # Fetch from the conversation store manager or create a new one if it doesn't exist
#     conv_store = conv_store_manager.get_store(user_id, connectRequest.conversation_id, connectRequest.connection_id)

#     # First, get the 
    
#     # Process the message and generate a response

#     ai_mock_response = "This is a mock AI response"  # Placeholder for AI response generation logic
#     mock_token_count = 42

#     conv_store.add_chat(
#         message=connectRequest.message,
#         timestamp=datetime.now()
#     )


#     # Here you would typically call your service layer to handle the business logic
#     # For now, we'll just echo the message back
#     response_data = PersonaChatResponse(
#         user_message=chatRequest.message,
#         ai_response="This is a mock AI response",
#         timestamp="2023-01-01T00:00:00Z",
#         session_number=1,
#         conversation_id="conv_123"
#     )

#     return response_data
# --------- stop

# This is not websocket route, but a regular HTTP POST route to set the AI companion for the conversation
# Set the ai companion for the conversation and return the status 200 OK response
@router.post("/set_companion", response_description="Set AI companion dto for the conversation")
async def set_ai_companion(request: Request, ai_companion_dto: AiCompanionDto, response: SetAiCompanionResponse):
    user_id = request.headers.get("uid")
    if not user_id:
        # response.status_code = 400  # Bad Request
        # return {"error": "User ID is required"}
        raise HTTPException(status_code=400, detail="User ID is required")
    
    # # You could also enforce these validations in the AiCompanionDto class using Pydantic validators.
    # # This is an example of manual validation here:
    # if not ai_companion_dto.name or len(ai_companion_dto.name) > 50:
    #     response.status_code = 400  # Bad Request
    #     return {"error": "AI companion name is required and should not exceed 50 characters"}
    # if ai_companion_dto.age < 18:
    #     response.status_code = 400  # Bad Request
    #     return {"error": "AI companion age must be 18 or older"}

    try:
        # Create the conversation in the mongodb
        conv_id = await mdb_manager.create_ai_companion(user_id, ai_companion_dto, datetime.now())
        # For now, just return 200 OK with a success message
        return {"status": "success", "conversation_id": conv_id}
    except HTTPException as http_exc:
        # response.status_code = http_exc.status_code
        # return {"error": http_exc.detail}
        raise http_exc
    except Exception as e:
        # response.status_code = 500
        # return {"error": str(e)}
        raise HTTPException(status_code=500, detail=str(e))