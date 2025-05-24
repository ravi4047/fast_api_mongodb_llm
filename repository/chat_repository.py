from fastapi import HTTPException
from mdb.db_manager import DatabaseManager
import logging
from datetime import datetime
import logging
from mdb.db_manager import db_manager ## Note, this must be initialized.

logger = logging.getLogger(__name__)

class ChatRepository:
    """Chat-related database operations"""

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db = db_manager

    async def add_message(self, user_id: str, message: str, is_user: bool)-> None:
        """Add a message to chat history"""
        try:
            await self.db.chat_history.insert_one({
                "user_id": user_id,
                "message": message,
                "is_user": is_user,
                "timestamp": datetime.utcnow()
            })
        except Exception as e:
            logger.error(f"Error adding chat message: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to save message")
        
# Initialize repositories
chat_repo = ChatRepository(db_manager)