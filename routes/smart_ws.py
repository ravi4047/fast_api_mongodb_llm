from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
import json
# from chatbot.react_chatbot import ReActDatingChatbot
from dto.chat_request_dto import ChatRequest
from main_old import chatbot, db_manager
from model.chat_prompt import ChatPrompt
from datetime import datetime

app = APIRouter()

## 🤔🤔 The whole thing is why should I save 2 times and not just one time? Please help me.
## Saving 2 times can help me to - 
## - confirm retrying
## - or if server gets crashed or I don't know
## - But during halting, I will try to save it whole.
## - During exception, Hmmm I shouldn't save it.
## --- Wait, so how should I save it?? 

# ==================== SMART STREAMING ENDPOINT ====================

@app.post("/chat/smart")
async def chat_smart_stream(request: Request, chatRequest: ChatRequest):

    uid = request.headers.get("uid")

    if uid is None:
        ## In actual way, i.e. API Gateway way it's not possible
        raise HTTPException(status_code=400)

    """Smart streaming that adapts to message complexity"""
    
    async def generate_smart_stream():
        full_response = ""
        title = ""
        conversation_id = ""
        timestamp = datetime.now()
        
        ## This is the last interaction
        chatPromptId = ""

        try:

            # Dropped this idea of saving early -------------- --------------------- start
            # # Save user message
            # user_message = ChatMessage(
            #     user_id=request.user_id,
            #     content=request.message,
            #     is_user=True
            # )

            # #### 🤔🤔🤔🤔 I still don't know why save_chat_message twice.
            # ## He also said to save it separately, but can't really convince me why https://claude.ai/chat/302f679b-d4c3-4726-9640-c96aa52d5068
            # await db_manager.save_chat_message(user_message)
            # Dropped this idea of saving early -------------- --------------------- stop
            
            # Process with smart streaming

            async for chunk in chatbot.process_message_smart(uid, chatRequest.message):
                yield f"data: {json.dumps(chunk)}\n\n"

                # Collect title for saving it in a conversation
                if chunk.get("type") == "title":
                    conversation_id = await db_manager.add_conversation(title, uid, timestamp)
                # Collect full response for saving
                if chunk.get("type") == "response" and chunk.get("is_final"):
                    full_response = chunk.get("full_content", "")
            
            # Save bot response
            ### 🤔🤔 We are saving it anyhow. Even half response. But complete one. Should I save the error? Becaues now I am thinking 
            ### that it's not good, technically.
            # if full_response:
            #     bot_message = ChatMessage(
            #         user_id=request.user_id,
            #         content=full_response,
            #         is_user=False
            #     )
            #     await db_manager.save_chat_message(bot_message)
                
        except Exception as e:
            error_chunk = {
                "type": "error",
                "content": f"I encountered an error: {str(e)}",
                "is_final": True
            }
            yield f"data: {json.dumps(error_chunk)}\n\n"

        finally:
            ## 👉👉 I will save here. I am totally skeptical of saving it in the database twice.
            ## 👉 It includes save the error one also + the halted ones whatever has been yielded that is chunked out.
            # I was also thinking about it + this guy also told to do that https://claude.ai/chat/302f679b-d4c3-4726-9640-c96aa52d5068

            # I am not in a mood to create the object here.
            # chat_prompt = ChatPrompt(
            #     conversation_id=conversation_id,
            #     timestamp=timestamp,
            #     ai_content=full_response,
            #     user_prompt=request.message,
            # )
            chatPromptId = await db_manager.save_chat_prompt(conv_id=conversation_id, uid=uid, user_prompt=chatRequest.message, ai_prompt=full_response, timestamp=timestamp)
            yield f"data: {json.dumps({"chat_id": chatPromptId})}"
    
    return StreamingResponse(
        generate_smart_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        }
    )

# ==================== WEBSOCKET FOR FLUTTER ==================== 👉👉 Websocket one is not needed. It's an overkill
                                                                        # -> https://claude.ai/chat/1760f327-87e7-41f0-b7b0-8ed9541afc65

# @app.websocket("/chat/ws/{user_id}")
# async def websocket_smart_chat(websocket: WebSocket, user_id: str):
#     """WebSocket with intelligent streaming strategy"""
#     await manager.connect(websocket, user_id)
    
#     try:
#         while True:
#             # Receive message from Flutter
#             data = await websocket.receive_text()
#             message_data = json.loads(data)
            
#             # Process with smart streaming
#             full_response = ""
#             async for chunk in chatbot.process_message_smart(user_id, message_data["message"]):
#                 await manager.send_message(user_id, chunk)
                
#                 if chunk.get("type") == "response" and chunk.get("is_final"):
#                     full_response = chunk.get("full_content", "")
            
#             # Save messages
#             user_message = ChatMessage(user_id=user_id, content=message_data["message"], is_user=True)
#             await db_manager.save_chat_message(user_message)
            
#             if full_response:
#                 bot_message = ChatMessage(user_id=user_id, content=full_response, is_user=False)
#                 await db_manager.save_chat_message(bot_message)
            
#     except WebSocketDisconnect:
#         manager.disconnect(user_id)