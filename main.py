from fastapi import FastAPI
from contextlib import asynccontextmanager
# from routes.conversations import router as convRouter
# from routes.chat import router as chatRouter
# from routes.bio_maker import router as bioRouter
from routes import bio_maker, chat, conversations
from mdb.db_manager import DatabaseManager
from configuration import DB_NAME, EMBEDDING_MODEL , GROQ_API_KEY, LLAMA_MODEL, MONGODB_URI
from chatbot.smart_streaming_chatbot import SmartStreamingChatbot

from chatbot.bio_bot import BioBot

import logging

logger = logging.getLogger(__name__)

chatbot = None
biobot = None
db_manager = DatabaseManager()

@asynccontextmanager
async def lifespan(app:FastAPI):
    try:
        if DB_NAME is None or EMBEDDING_MODEL is None or MONGODB_URI is None or LLAMA_MODEL is None or GROQ_API_KEY is None:
            raise

        await db_manager.connect(MONGODB_URI, DB_NAME)
        global chatbot
        chatbot =  SmartStreamingChatbot(db_manager, "")

        global biobot
        biobot = BioBot()

        logger.info("Application startup completed")
        yield
    except Exception as e:
        print(e)
    finally:
        pass

app = FastAPI(lifespan=lifespan)

app.include_router(chat.router, tags=["chat"], prefix="/chat")
app.include_router(conversations.router, tags=["conversation"], prefix="/conversation")
app.include_router(bio_maker.router, tags=["bio maker"], prefix="/bio")