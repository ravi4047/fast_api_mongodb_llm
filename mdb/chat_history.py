# from datetime import datetime

# from typing import List, Dict

# ## 👉👉 This is the new one for the Database Manager and Repository. So not needed. We will handle it in Repository.

# # Chat history with AI
# async def add_chat_history(user_id: str, message: str, is_user: bool, ) -> None:
#     """Add a message to the chat history between user and AI."""
#     await chat_history_collection.insert_one({
#         "user_id": user_id,
#         "message": message,
#         "is_user": is_user,
#         "timestamp": datetime.utcnow()
#     })

# async def get_chat_history(user_id: str, limit: int = 20) -> List[Dict]:
#     """Get recent chat history for a user."""
#     cursor = chat_history_collection.find(
#         {"user_id": user_id}
#     ).sort("timestamp", -1).limit(limit)
    
#     # Return in chronological order
#     history = await cursor.to_list(length=limit)
#     return list(reversed(history))