from fastapi import FastAPI, Depends, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from mdb.setup import setup_mongodb2
from llm.llm import setup_llm
from llm.embedding import setup_embedding
from routes.chat import router as chatRouter
# from agent.graph import build_graph
from pymongo import MongoClient
from langgraph.checkpoint.mongodb import MongoDBSaver
from token_and_rate_limiting_system.token_limiting import limit_settings

from configuration import DB_NAME, EMBEDDING_MODEL , GROQ_API_KEY, LLAMA_MODEL, MONGODB_URI

from mdb.db_manager import DatabaseManager

# from chatbot.react_chatbot import ReActDatingChatbot # I am using react smart real streaming
from chatbot.smart_streaming_chatbot import SmartStreamingChatbot

import logging

from configuration import DB_NAME

logger = logging.getLogger(__name__)

# from dotenv import dotenv_values
# config = dotenv_values(".env")

app = FastAPI()

# https://claude.ai/chat/74a39efa-66d4-41a6-9240-38eea7937760
# Global variable for the client
## 🤔🤔 Now I am confused, where should the global variables be initialized i.e. object be created? Should it be initialized in
##  the main.py i.e. the beginning file of the fastapi project or inside the file where their classes are created. I want to follow singleton
## approach thus creating robust architect
## -->> Solution: To follow singleton approach, use in main.py
mongo_client = None

db_manager = DatabaseManager()
# chatbot = ReActDatingChatbot(db_manager, "open-api-key")
chatbot = None

# async def get_db():
def get_db():
    """Dependency to get database connection."""
    if not mongo_client:
        raise Exception("MongoDB client not initialized")
    return mongo_client.my_db

@asynccontextmanager
async def lifespan(app:FastAPI):
    # db = setup_mongodb2(config["MONGODB_ATLAS_URI"], config["MONGODB_NAME"])

    ## How should I add strictness to the variable and make sure it's not None.
    try:
        # dbName = config["MONGODB_NAME"]
        # mongodbUri = config["MONGODB_ATLAS_URI"]
        # llamaModel = config["LLAMA_MODEL"]
        # groqApiKey = config["GROQ_API_KEY"]
        # embeddingModel = config["EMBEDDING_MODEL"]

        # if dbName is None or mongodbUri is None or llamaModel is None or groqApiKey is None or embeddingModel is None:
        #     raise
        if DB_NAME is None or EMBEDDING_MODEL is None or MONGODB_URI is None or LLAMA_MODEL is None or GROQ_API_KEY is None:
            raise

        global mongo_client ### ⭐⭐ This is very important.
        mongo_client = MongoClient(MONGODB_URI) ### 👈👈 Dude this is not initializing the global variable. You have to specify the 
                                                ## global keyword for that.

        db = mongo_client[DB_NAME]

        ## Collections
        # userCollection = db["playerCollection"]

        llm = setup_llm(LLAMA_MODEL, GROQ_API_KEY)

        # Initialize the MongoDB checkpointer
        memory = MongoDBSaver(mongo_client)
        # graph = build_graph(llm, memory, db)

        embedding = setup_embedding(EMBEDDING_MODEL) # Embedding is needed for memory purpose to retain the data or related information.

        # Store both
        app.state.db = db
        app.state.llm = llm
        # app.state.graph = graph
        app.state.embedding = embedding
        
        # https://claude.ai/chat/3189db2e-a00b-489b-8118-b1a5d97f8dc5
        ## Newest one
        await db_manager.connect(MONGODB_URI, DB_NAME)
        logger.info("Application startup completed")

        global chatbot
        chatbot =  SmartStreamingChatbot(db_manager, "")

        yield
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        raise
    finally:
        # Shutdown
        await db_manager.disconnect()
        logger.info("Application shutdown completed")

fastAPI = FastAPI(lifespan=lifespan)

app.include_router(chatRouter, tags=["chat"], prefix="/chat")

# FastAPI Integration for Multi-Domain Support
# Update your FastAPI endpoint to handle the multi-domain architecture:

########## ----------------------------------------------------------------------------------------- ###################
# @app.post("/dating-assistant/")
# async def dating_assistant(query: UserQuery):
#     # Create or retrieve conversation thread
#     thread_id = f"user_{query.user_id}"
    
#     try:
#         # Get existing state or initialize new one
#         state = main_graph_instance.get_state(thread_id)

#         ## 👉👉 I don't think this idea is good. There can be multiple servers.

#     except:
#         state = {
#             "user_id": query.user_id,
#             "conversation_history": []
#         }
    
#     # Update state with new query
#     state["user_query"] = query.query
    
#     # Process through graph
#     result = main_graph_instance.invoke(state, thread_id=thread_id)
    
#     return {"response": result["response"], "domain": result["identified_domain"]}
########## ----------------------------------------------------------------------------------------- ###################

@app.get("/usage/{user_id}")
async def get_usage(user_id: str, db = Depends(get_db)):
    """Get usage statistics for a user."""
    usage_dict = await db.user_usage.find_one({"user_id": user_id})
    if not usage_dict:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Clean up the response by removing internal fields
    usage_dict.pop("_id", None)
    
    return {
        "user_id": usage_dict["user_id"],
        "tokens": {
            "minute": {
                "used": usage_dict["tokens_used_minute"],
                "limit": limit_settings.tokens_per_minute,
                "reset_at": usage_dict["minute_reset_time"]
            },
            "hour": {
                "used": usage_dict["tokens_used_hour"],
                "limit": limit_settings.tokens_per_hour,
                "reset_at": usage_dict["hour_reset_time"]
            },
            "day": {
                "used": usage_dict["tokens_used_day"],
                "limit": limit_settings.tokens_per_day,
                "reset_at": usage_dict["day_reset_time"]
            }
        },
        "rate": {
            "requests_minute": {
                "used": usage_dict["request_count_minute"],
                "limit": limit_settings.requests_per_minute,
                "reset_at": usage_dict["minute_reset_time"]
            }
        }
    }

# Health Checks: Add MongoDB health check endpoint

@app.get("/health")
# async def health_check(db: AsyncIOMotorClient = Depends(get_db)): ## motor library is deprecated. Not to be used.
async def health_check(db = Depends(get_db)):
    try:
        # Ping the server
        await db.admin.command('ping')
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}
    

### -------------------- -------------------- ---------------------- ----------------------
# Endpoint for handling rate limit errors
@app.exception_handler(status.HTTP_429_TOO_MANY_REQUESTS)
async def rate_limit_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "error": {
                "message": exc.detail,
                "type": "rate_limit_error",
                "code": 429
            }
        },
    )