import os
from dotenv import dotenv_values
config = dotenv_values(".env")

DB_NAME = config["MONGODB_NAME"]
MONGODB_URI = config["MONGODB_ATLAS_URI"]
LLAMA_MODEL = config["LLAMA_MODEL"]
GROQ_API_KEY = config["GROQ_API_KEY"]
EMBEDDING_MODEL = config["EMBEDDING_MODEL"]

## Dynamodb
DDB_REGION_NAME=config["DDB_REGION_NAME"]
DDB_ACCESS_KEY_ID=config["DDB_ACCESS_KEY_ID"]
DDB_SECRET_ACCESS_KEY=config["DDB_SECRET_ACCESS_KEY"]

# Content filtering settings
MAX_TOXICITY_SCORE = float(os.getenv("MAX_TOXICITY_SCORE", "0.7"))
BLOCKED_TOPICS = [
    "explicit sexual content", 
    "graphic violence", 
    "hate speech", 
    "harassment",
    "non-consensual content"
]

# Collection names
PROFILES_COLLECTION = "profiles"
MATCHES_COLLECTION = "matches"
MESSAGES_COLLECTION = "messages"
CHAT_HISTORY_COLLECTION = "chat_history"
FEEDS_HISTORY_COLLECTION = "feeds_history"

# Azure OpenAI settings
AZURE_OPENAI_ENDPOINT="azure-openai"
AZURE_OPENAI_API_KEY="azure-openai-api-key"
AZURE_OPENAI_DEPLOYMENT_NAME="azure-openai-deployment-name"