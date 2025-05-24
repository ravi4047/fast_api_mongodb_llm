from fastapi import HTTPException
from mdb.db_manager import DatabaseManager
import logging
from datetime import datetime
import logging
from mdb.db_manager import db_manager ## Note, this must be initialized.

logger = logging.getLogger(__name__)

class FeedHistory:
    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db = db_manager

    async def get_feed_history(self, uid:str, limit: int):
        """Get profile by ID with error handling."""
        try:
            result = await self.db.feeds_history.find_one(filter={"user": 234})
            return result
        except Exception as e:
            logger.error(f"Error adding feed message: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to save feeds")

feed_history_repo = FeedHistory(db_manager)