# MongoDB Configuration

## For local development
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=ai_service
MONGO_MIN_POOL_SIZE=5
MONGO_MAX_POOL_SIZE=50

# Limit Settings

## Token limits
LIMIT_TOKENS_PER_MINUTE=10000
LIMIT_TOKENS_PER_HOUR=50000
LIMIT_TOKENS_PER_DAY=200000

## Rate limits
LIMIT_REQUESTS_PER_MINUTE=60

## Concurrency limits
LIMIT_MAX_CONCURRENT_SESSIONS=100

# Server Settings
HOST=0.0.0.0
PORT=8000
DEBUG=true
LOG_LEVEL=INFO


pip install fastapi uvicorn motor tiktoken langgraph pydantic-settings

## So motor is deprecated.