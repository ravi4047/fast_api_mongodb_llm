from fastapi import APIRouter, WebSocket
from utils.connection_manager import manager
from main_old import chatbot
import json 

router = APIRouter()

# https://claude.ai/chat/bd16e0ac-f26c-4874-96da-dfa0b3b534e0

@router.websocket("/chat/ws/{user_id}")
async def websocket_chat(websocket:WebSocket, user_id:str):
    """WebSocket for Flutter app with true streaming"""
    await manager.connect(websocket, user_id)

    try:
        while True:
            # Receive message from flutter
            data = await websocket.receive_text()
            message_data = json.loads(data)

            # Save user message
            # user_message = ChatMessage(
            #     user_id=user_id,
            #     content=message_data["message"],
            #     is_user=True
            # )
            # await db_manager.save_chat_message(user_message)
            ### 🤔👉I don't want to save one by one

            # Stream AI response
            full_response = ""
            async for chunk in chatbot.process_message_stream(user_id, message_data["message"]):
                await manager.send_message(user_id, chunk)
                

