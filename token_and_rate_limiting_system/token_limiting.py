from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from contextlib import asynccontextmanager
from typing import Dict, Any, Optional, List, Literal, LiteralString
import time
import tiktoken
from datetime import datetime, timedelta
import asyncio
from uuid import uuid4
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============= Settings =============
class MongoSettings(BaseSettings):
    uri: str = "mongodb://localhost:27017"
    db_name: str = "ai_service"
    min_pool_size: int = 5
    max_pool_size: int = 50
    
    class Config:
        env_prefix = "MONGO_"

class LimitSettings(BaseSettings):
    # Token limits
    tokens_per_minute: int = 10000
    tokens_per_hour: int = 50000
    tokens_per_day: int = 200000
    
    # Rate limits
    requests_per_minute: int = 60
    
    # Concurrency limits
    max_concurrent_sessions: int = 100
    
    class Config:
        env_prefix = "LIMIT_"

mongo_settings = MongoSettings()
limit_settings = LimitSettings()

# ============= MongoDB Models =============
class UserUsage(BaseModel):
    user_id: str
    tokens_used_minute: int = 0
    tokens_used_hour: int = 0 
    tokens_used_day: int = 0
    last_request_time: datetime = Field(default_factory=datetime.now)
    minute_reset_time: datetime = Field(default_factory=datetime.now)
    hour_reset_time: datetime = Field(default_factory=lambda: datetime.now() + timedelta(hours=1))
    day_reset_time: datetime = Field(default_factory=lambda: datetime.now() + timedelta(days=1))
    request_count_minute: int = 0
    
    class Config:
        arbitrary_types_allowed = True

# ============= Token Counter =============
class TokenCounter:
    def __init__(self, model_name="gpt-3.5-turbo"):
        """Initialize the token counter with the appropriate encoding."""
        self.encoder = tiktoken.encoding_for_model(model_name)
    
    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in the given text."""
        if not text:
            return 0
        return len(self.encoder.encode(text))
    
    def count_message_tokens(self, messages: List[Dict[str, str]]) -> int:
        """Count tokens in a list of chat messages."""
        token_count = 0
        for message in messages:
            # Count tokens in the message content
            if "content" in message and message["content"]:
                token_count += self.count_tokens(message["content"])
            # Add a small overhead for message format
            token_count += 4  # Rough approximation for message overhead
        return token_count

# ============= Concurrency Manager =============
class ConcurrencyManager:
    def __init__(self, max_concurrent: int):
        self.max_concurrent = max_concurrent
        self.active_sessions = 0
        self._lock = asyncio.Lock()
    
    async def acquire(self):
        """Attempt to acquire a session slot."""
        async with self._lock:
            if self.active_sessions >= self.max_concurrent:
                return False
            self.active_sessions += 1
            return True
    
    async def release(self):
        """Release a session slot."""
        async with self._lock:
            if self.active_sessions > 0:
                self.active_sessions -= 1

# ============= Usage Tracker =============
class UsageTracker:
    def __init__(self, db, token_counter, concurrency_manager):
        self.db = db
        self.token_counter = token_counter
        self.concurrency_manager = concurrency_manager
        self.collection = db.user_usage
    
    async def track_request(self, user_id: str, request_data: Dict[str, Any])->tuple[bool, str|None]:
        """
        Track a request and check if it's within limits.
        Returns True if request is allowed, False otherwise.
        Also updates usage statistics.
        """
        # Check if we can handle another concurrent session
        if not await self.concurrency_manager.acquire():
            return False, "Maximum concurrent sessions reached"
        
        try:
            # Get or create user usage record
            usage = await self.get_or_create_usage(user_id)
            now = datetime.now()
            
            # Reset counters if time periods have elapsed
            if now > usage.minute_reset_time:
                usage.tokens_used_minute = 0
                usage.request_count_minute = 0
                usage.minute_reset_time = now + timedelta(minutes=1)
            
            if now > usage.hour_reset_time:
                usage.tokens_used_hour = 0
                usage.hour_reset_time = now + timedelta(hours=1)
            
            if now > usage.day_reset_time:
                usage.tokens_used_day = 0
                usage.day_reset_time = now + timedelta(days=1)
            
            # Check rate limit
            if usage.request_count_minute >= limit_settings.requests_per_minute:
                return False, "Rate limit exceeded"
            
            # Count tokens in the request
            token_count = 0
            if "messages" in request_data:
                token_count = self.token_counter.count_message_tokens(request_data["messages"])
            elif "prompt" in request_data:
                token_count = self.token_counter.count_tokens(request_data["prompt"])
            
            # Check token limits
            if usage.tokens_used_minute + token_count > limit_settings.tokens_per_minute:
                return False, "Minute token limit exceeded"
            
            if usage.tokens_used_hour + token_count > limit_settings.tokens_per_hour:
                return False, "Hour token limit exceeded"
            
            if usage.tokens_used_day + token_count > limit_settings.tokens_per_day:
                return False, "Daily token limit exceeded"
            
            # Update usage
            usage.tokens_used_minute += token_count
            usage.tokens_used_hour += token_count
            usage.tokens_used_day += token_count
            usage.request_count_minute += 1
            usage.last_request_time = now
            
            # Save to DB
            await self.update_usage(usage)
            
            return True, None
            
        except Exception as e:
            logger.error(f"Error tracking usage: {e}")
            await self.concurrency_manager.release()
            return False, f"Error tracking usage: {str(e)}"
    
    async def track_response(self, user_id: str, response_data: Dict[str, Any]):
        """Track tokens in the response."""
        try:
            usage = await self.get_or_create_usage(user_id)
            token_count = 0
            
            # Count tokens in the response
            if "choices" in response_data and response_data["choices"]:
                choice = response_data["choices"][0]
                if "message" in choice and "content" in choice["message"]:
                    token_count = self.token_counter.count_tokens(choice["message"]["content"])
            
            # Update usage
            usage.tokens_used_minute += token_count
            usage.tokens_used_hour += token_count
            usage.tokens_used_day += token_count
            
            # Save to DB
            await self.update_usage(usage)
            
        except Exception as e:
            logger.error(f"Error tracking response: {e}")
        finally:
            await self.concurrency_manager.release()
    
    async def get_or_create_usage(self, user_id: str) -> UserUsage:
        """Get or create a user usage record."""
        usage_dict = await self.collection.find_one({"user_id": user_id})
        if not usage_dict:
            usage = UserUsage(user_id=user_id)
#             await self.collection.insert_one(usage.dict()) The method "dict" in class "BaseModel" is deprecated
#   The `dict` method is deprecated; use `model_dump` instead
            await self.collection.insert_one(usage.model_dump())
            return usage
        
        # Convert MongoDB document to UserUsage model
        usage_dict["id"] = str(usage_dict.pop("_id"))
        return UserUsage(**usage_dict)
    
    async def update_usage(self, usage: UserUsage):
        """Update user usage in the database."""
        # usage_dict = usage.dict() #   The `dict` method is deprecated; use `model_dump` instead
        usage_dict = usage.model_dump()
        await self.collection.update_one(
            {"user_id": usage.user_id},
            {"$set": usage_dict},
            upsert=True
        )

# ============= FastAPI App Setup =============
# Global variables
mongo_client = None
token_counter = None
concurrency_manager = None
usage_tracker = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize resources on startup
    global mongo_client, token_counter, concurrency_manager, usage_tracker
    
    logger.info("Initializing MongoDB connection...")
    mongo_client = AsyncIOMotorClient(
        mongo_settings.uri,
        minPoolSize=mongo_settings.min_pool_size,
        maxPoolSize=mongo_settings.max_pool_size,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=10000,
        retryWrites=True
    )
    db = mongo_client[mongo_settings.db_name]
    
    # Create indexes
    await db.user_usage.create_index("user_id", unique=True)
    
    logger.info("Initializing token counter...")
    token_counter = TokenCounter()
    
    logger.info("Initializing concurrency manager...")
    concurrency_manager = ConcurrencyManager(limit_settings.max_concurrent_sessions)
    
    logger.info("Initializing usage tracker...")
    usage_tracker = UsageTracker(db, token_counter, concurrency_manager)
    
    yield
    
    # Clean up resources on shutdown
    logger.info("Shutting down MongoDB connection...")
    if mongo_client:
        mongo_client.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= Dependencies =============
async def get_db():
    """Dependency to get database connection."""
    if not mongo_client:
        raise HTTPException(status_code=500, detail="Database not initialized")
    return mongo_client[mongo_settings.db_name]

async def get_user_id(request: Request):
    """
    Get user ID from request. In a real application,
    this would come from authentication middleware.
    """
    # In a real app, extract from auth token
    # For demo, we'll use header or generate one
    user_id = request.headers.get("X-User-ID")
    if not user_id:
        user_id = f"anon-{uuid4()}"
    return user_id

async def check_limits(request: Request, user_id: str = Depends(get_user_id)):
    """Check if the request is within limits."""
    request_data = {}
    body = await request.json()

    if usage_tracker is None:
        ## 🤔🤔🤔 What exception should I throw when things are not initialized or None in python fastapi
        ## ✅ Ans - Use ValueError
        raise ValueError("Expected a non-None value, but got None.")
    
    allowed, message = await usage_tracker.track_request(user_id, body)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=message
        )
    
    return user_id

# ============= Routes =============
@app.get("/health")
async def health_check(db = Depends(get_db)):
    try:
        # Ping the server
        await db.command("ping")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}

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

# Example of a limited endpoint
@app.post("/chat")
async def chat_endpoint(
    request: Request,
    user_id: str = Depends(check_limits)  # This will enforce the limits
):
    """
    Protected chat endpoint that enforces token limits.
    This is where you'd integrate with LangGraph.
    """
    request_body = await request.json()
    
    # Here you would process the request with LangGraph
    # For demo purposes, we'll just echo back the request with a simulated response
    response_data = {
        "id": f"chatcmpl-{uuid4()}",
        "object": "chat.completion",
        "created": int(time.time()),
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": f"This is a simulated response to: {request_body.get('messages', [{}])[-1].get('content', '')}"
                },
                "finish_reason": "stop"
            }
        ]
    }

    if usage_tracker is None:
        raise ValueError("Expected a non-None value, but got None.")
    
    # Track the response tokens
    await usage_tracker.track_response(user_id, response_data)
    
    return response_data

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
