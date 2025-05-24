from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
import logging
from typing import Dict, List, Any

# Import components
from token_limiting import (
    lifespan as token_lifespan,
    token_counter, 
    concurrency_manager,
    usage_tracker,
    limit_settings,
    mongo_settings
)
from langgraph_integration import LangGraphManager, GraphState

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
mongo_client = None
graph_manager = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize MongoDB and token tracking components
    async with token_lifespan(app):
        # Initialize our LangGraph manager
        global graph_manager
        graph_manager = LangGraphManager(mongo_client, token_counter)
        
        logger.info("Application initialized and ready")
        yield
        
        logger.info("Shutting down application")

# Create the application
app = FastAPI(
    title="AI Service API",
    description="API for AI services with token limiting and LangGraph integration",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers from components
from token_limiting import app as token_app

# Define API routes
@app.get("/")
async def root():
    return {
        "message": "AI Service API",
        "status": "online",
        "version": "1.0.0"
    }

# Create a router for the chat endpoints
router = APIRouter(prefix="/api/v1", tags=["AI Services"])

@router.post("/chat")
async def chat_endpoint(data: Dict[str, Any]):
    """
    Process a chat request using LangGraph.
    
    This endpoint:
    1. Validates and counts tokens
    2. Checks if the user is within limits
    3. Processes the request through the LangGraph workflow
    4. Tracks usage
    5. Returns the response
    """
    user_id = data.get("user_id", "anonymous")
    messages = data.get("messages", [])
    
    if not graph_manager:
        return {"error": "Service not initialized"}
    
    # Process through LangGraph
    result = await graph_manager.run(
        user_id=user_id,
        messages=messages
    )
    
    return result

# Mount the endpoints
app.include_router(token_app)
app.include_router(router)

### 
@router.post("/conversation")
async def conversation_endpoint(data: Dict[str, Any]):
    """
    These are direct conversation.
    """
    


# Main entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
