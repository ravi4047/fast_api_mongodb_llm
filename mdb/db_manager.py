from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase
from typing import Optional
import logging
from model.chat_prompt import ChatPrompt, Conversation
from model.user_profile import UserProfile
from fastapi import HTTPException
from datetime import datetime

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
    def chat_prompts(self):
        if self.database is None:
            raise
        return self.database["chat_prompts"]

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
    
    @property
    def bot_conversations(self):
        if self.database is None:
            raise
        return self.database["bot_conversations"]
    
    ## Note, here we won't handle any object parameter or error. This is just for database operation. All error handling stuff 
    ## will be done in repository/controller/nodes/tools etc.

    ## Chat prompts --------------------------------------------------------- START ---------------------------
    def save_chat_history(self, data):
        return self.chat_history.insert_one(data)
    
    ## Claude is throwing Http 500 exception for database error. 404 for not found one.
    # async def save_chat_prompt(self, chat_prompt: ChatPrompt)->str:
    async def save_chat_prompt(self, conv_id: str, uid: str, user_prompt: str, ai_prompt: str, timestamp: datetime)->str:
        try:
            # chat_prompt = ChatPrompt(
            #     conversation_id=conv_id,
            #     uid=uid,
            #     ai_content=ai_prompt,
            #     user_prompt=user_prompt,
            #     timestamp=timestamp
            # )
            chat_prompt = ChatPrompt.create(conv_id=conv_id, timestamp=timestamp, ai_content=ai_prompt, user_prompt=user_prompt)
            result = await self.chat_prompts.insert_one(chat_prompt)
            return result.inserted_id
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error in inserting chat prompt {e}")
        
    async def paging_chat_prompts(self, conv_id, page: int, per_page:int)->list[ChatPrompt]:
        # skip = page*per_page
        ## I think make the page > 0, hence
        skip = (page-1)*per_page
        try:
            result = await self.chat_prompts.find({"conversation_id": conv_id}).skip(skip).limit(per_page).to_list()
            # return result ## I think I should parse it.
            return [ChatPrompt(**chat) for chat in result]
        except Exception as e:
            raise HTTPException(status_code=500)
    ## Chat prompts --------------------------------------------------------- STOP ---------------------------    
    
    ## Conversation stuff ------------------------------------------------------------------ START --------------------
    async def add_conversation(self, title:str, user_id:str, timestamp: datetime):
        try:
            print(title, user_id, timestamp)
            # conv = Conversation(uid=user_id, title=title, timestamp=timestamp)
            conv = Conversation.create(uid=user_id, title=title, timestamp=timestamp)
            result = await self.bot_conversations.insert_one(document=conv)
            return result.inserted_id
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error in inserting conversation prompt {e}")
        
    async def paging_conversations(self, user_id, page: int, per_page:int)->list[Conversation]:
        # skip = page*per_page
        ## I think make the page > 0, hence
        skip = (page-1)*per_page
        try:
            result = await self.bot_conversations.find({"uid": user_id}).skip(skip).limit(per_page).to_list()
            # return list
            return [Conversation(**conv) for conv in result]
        except Exception as e:
            raise HTTPException(status_code=500)
    ## Conversation stuff ------------------------------------------------------------------ STOP --------------------

    ## Profile stuff ----------- start --------------
    async def get_user_profile(self, uid:str)->UserProfile:
        try:
            print("uid", uid)
            # conv = Conversation(uid=user_id, title=title, timestamp=timestamp)
            # conv = Conversation.create(uid=user_id, title=title, timestamp=timestamp)
            # result = await self.bot_conversations.insert_one(document=conv)
            # return result.inserted_id
            result = await self.profiles.find_one({"uid": uid})
            # if result is None: # or
            if not result: # 👉👉 That means none is treated as negative 
                raise HTTPException(status_code=404, detail="Error in inserting conversation prompt {e}")
            return result
        except HTTPException as http_exc:
            raise http_exc # Pass HTTP exceptions directly
        ## 👉👉👉👉 This will return my exceptions i.e. 404 is None

        except Exception as e:
            raise HTTPException(status_code=500, detail="Error in fetching a user profile")
    ## Profile stuff ----------- stop --------------


# # Global instance
# db_manager = DatabaseManager()
### I am initializing it in main.py as Global instance