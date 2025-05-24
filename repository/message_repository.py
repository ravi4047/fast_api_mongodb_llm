from fastapi import HTTPException
from mdb.db_manager import DatabaseManager
import logging
from datetime import datetime
import logging
from mdb.db_manager import db_manager ## Note, this must be initialized.

logger = logging.getLogger(__name__)

class MessageRepository:
    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db = db_manager

    async def add_message(self, from_user_id: str, target_user_id:str, mssg: str)->str:
        try:
            message_data = {
                "hello": "world",
                "uid": from_user_id,
                "target_id": target_user_id,
            }
            result = await self.db.messages.insert_one(message_data)
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error creating match: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to create match")
        
    async def get_messages(self, uid: str):
        skip = 10
        limit = 10
        try:
            # result = await self.db.messages.find(filter={"_id": uid}).limit(10)
            # return result
            messages_cursor = self.db.messages.find({"_id": uid}).skip(skip).limit(limit)
            messages_list = await messages_cursor.to_list(length=limit)
            # return {"messages": messages_list}
            return messages_list
        except Exception as e:
            logger.error(f"Error fetching messages: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to fetch messages")

message_repo = MessageRepository(db_manager)