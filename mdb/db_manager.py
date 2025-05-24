from pymongo import AsyncMongoClient, asynchronous
from pymongo.asynchronous.database import AsyncDatabase
from typing import Optional
import logging

logger = logging.getLogger(__name__)

## 👉 I don't know the right architecture. The Repository and object oriented is the recommended one I think.

# https://claude.ai/chat/3189db2e-a00b-489b-8118-b1a5d97f8dc5

class DatabaseManager:
    """Centralized database manager with connection lifecycle and error handling."""
    def __init__(self):
        self.client: Optional[AsyncMongoClient] = None
        self.database: Optional[AsyncDatabase] = None

    async def connect(self, mongodb_uri:str, database_name: str):
        """Initialize database connection."""
        try:
            self.client = AsyncMongoClient(mongodb_uri)
            # By default, AsyncMongoClient only connects to the database on its first operation.
            #  To explicitly connect before performing an operation, use aconnect():

            # client = await AsyncMongoClient().aconnect()
            ### 👉 That means the above ones are enough

            self.database = self.client[database_name]

            # Test the connection
            await self.client.admin.command('ping')
            logger.info(f"Connected to MongoDB: {database_name}")
        except Exception as e:
            raise

    async def disconnect(self):
        """Close database connection"""
        if self.client:
            await self.client.close()
            logger.info("Disconnected from MongoDB")

    # Database operations with error handling
    @property
    def profiles(self):
        if self.database is None:
            raise
        return self.database["profiles"]
    
    # Database operations with error handling
    @property
    def matches(self):
        if self.database is None:
            raise
        return self.database["matches"]
    
    @property
    def messages(self):
        if self.database is None:
            raise
        return self.database["messages"]
    
    @property
    def chat_history(self):
        if self.database is None:
            raise
        return self.database["chat_history"]
    
    @property
    def feeds_history(self):
        if self.database is None:
            raise
        return self.database["feeds_history"]
    
# Global instance
db_manager = DatabaseManager()