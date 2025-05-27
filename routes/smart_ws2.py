# from fastapi import APIRouter
# from fastapi.responses import StreamingResponse
# import json
# # from chatbot.react_chatbot import ReActDatingChatbot
# from main import chatbot
# app = APIRouter()

# @app.post("/chat/smart")
# async def chat_smart_stream(request: ChatRequest):
#     """Smart streaming with halt capability"""
    
#     async def generate_smart_stream():
#         try:
#             # Process with smart streaming
#             async for chunk in chatbot.process_message_smart(
#                 request.user_id, 
#                 request.message, 
#                 request.stream_id
#             ):
#                 yield f"data: {json.dumps(chunk)}\n\n"
                
#         except Exception as e:
#             error_chunk = {
#                 "type": "error",
#                 "content": f"Error: {str(e)}",
#                 "stream_id": request.stream_id,
#                 "is_final": True
#             }
#             yield f"data: {json.dumps(error_chunk)}\n\n"
    
#     return StreamingResponse(
#         generate_smart_stream(),
#         media_type="text/event-stream",
#         headers={
#             "Cache-Control": "no-cache",
#             "Connection": "keep-alive",
#             "X-Accel-Buffering": "no",  # Disable nginx buffering
#         }
#     )