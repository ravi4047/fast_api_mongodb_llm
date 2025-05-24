from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
from langgraph.graph import StateGraph
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from uuid import uuid4
import tiktoken

# ==================== LangGraph Integration ====================

class GraphState(BaseModel):
    """State object that gets passed between LangGraph nodes."""
    # Input data
    user_id: str
    messages: List[Dict[str, str]] = Field(default_factory=list)
    query_params: Dict[str, Any] = Field(default_factory=dict)
    
    # Processing state
    db_client: Optional[Any] = None
    token_usage: Dict[str, int] = Field(default_factory=lambda: {"prompt": 0, "completion": 0, "total": 0})
    
    # Results
    results: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True  # For the MongoDB client

class LangGraphManager:
    """Manager for LangGraph workflows with token tracking."""
    
    def __init__(self, db_client, token_counter):
        self.db_client = db_client
        self.token_counter = token_counter
        self.workflow = self._build_workflow()
    
    def _build_workflow(self):
        """Build and compile the workflow graph."""
        workflow = StateGraph(GraphState)
        
        # Define nodes
        workflow.add_node("check_limits", self.check_limits)
        workflow.add_node("process_query", self.process_query)
        workflow.add_node("generate_response", self.generate_response)
        workflow.add_node("track_usage", self.track_usage)
        
        # Define edges - a simple sequential flow with conditional
        workflow.add_conditional_edges(
            "check_limits",
            lambda state: "process_query" if not state.error else "track_usage"
        )
        workflow.add_edge("process_query", "generate_response")
        workflow.add_edge("generate_response", "track_usage")
        
        # Set entry and exit points
        workflow.set_entry_point("check_limits")
        
        return workflow.compile()
    
    async def check_limits(self, state: GraphState):
        """Check if the user is within limits."""
        try:
            # Access the usage collection
            collection = self.db_client.ai_service.user_usage
            
            # Get user usage
            usage = await collection.find_one({"user_id": state.user_id})
            
            if not usage:
                # New user, no need to check limits
                return state
            
            now = datetime.utcnow()
            
            # Count tokens in the current request
            prompt_tokens = self.token_counter.count_message_tokens(state.messages)
            state.token_usage["prompt"] = prompt_tokens
            
            # Check if user is over limits
            if now < usage.get("minute_reset_time", now) and \
               usage.get("tokens_used_minute", 0) + prompt_tokens > 10000:  # Example limit
                state.error = "Minute token limit exceeded"
            
            elif now < usage.get("hour_reset_time", now) and \
                 usage.get("tokens_used_hour", 0) + prompt_tokens > 50000:  # Example limit
                state.error = "Hour token limit exceeded"
            
            elif now < usage.get("day_reset_time", now) and \
                 usage.get("tokens_used_day", 0) + prompt_tokens > 200000:  # Example limit
                state.error = "Day token limit exceeded"
            
            # Add rate limit check
            elif now < usage.get("minute_reset_time", now) and \
                 usage.get("request_count_minute", 0) > 60:  # Example limit
                state.error = "Rate limit exceeded"
        
        except Exception as e:
            state.error = f"Error checking limits: {str(e)}"
        
        return state
    
    async def process_query(self, state: GraphState):
        """Process the user query."""
        # Here you would implement your business logic
        # For example, retrieving data from MongoDB
        try:
            collection = self.db_client.ai_service.conversations
            
            # Store the conversation in MongoDB
            conversation_id = str(uuid4())
            await collection.insert_one({
                "conversation_id": conversation_id,
                "user_id": state.user_id,
                "messages": state.messages,
                "created_at": datetime.utcnow()
            })
            
            # Add the conversation ID to the state
            state.results["conversation_id"] = conversation_id
            
        except Exception as e:
            state.error = f"Error processing query: {str(e)}"
        
        return state
    
    async def generate_response(self, state: GraphState):
        """Generate a response using an LLM."""
        if state.error:
            return state
            
        try:
            # Here you would call your LLM service
            # For demonstration, we'll simulate a response
            
            # Get the latest user message
            latest_message = state.messages[-1]["content"] if state.messages else ""
            
            # Simulate a response
            response = f"This is a response to: {latest_message}"
            
            # Count completion tokens
            completion_tokens = self.token_counter.count_tokens(response)
            state.token_usage["completion"] = completion_tokens
            state.token_usage["total"] = state.token_usage["prompt"] + completion_tokens
            
            # Add the response to the results
            state.results["response"] = {
                "role": "assistant",
                "content": response
            }
            
        except Exception as e:
            state.error = f"Error generating response: {str(e)}"
        
        return state
    
    async def track_usage(self, state: GraphState):
        """Track token usage in MongoDB."""
        try:
            collection = self.db_client.ai_service.user_usage
            
            # Ensure there's a user document
            now = datetime.now()
            
            # Define the update operation
            update_data = {
                "$inc": {
                    "tokens_used_minute": state.token_usage["total"],
                    "tokens_used_hour": state.token_usage["total"],
                    "tokens_used_day": state.token_usage["total"],
                    "request_count_minute": 1
                },
                "$set": {
                    "last_request_time": now
                },
                "$setOnInsert": {
                    "minute_reset_time": now.replace(second=0, microsecond=0).replace(minute=now.minute+1),
                    "hour_reset_time": now.replace(minute=0, second=0, microsecond=0).replace(hour=now.hour+1),
                    "day_reset_time": now.replace(hour=0, minute=0, second=0, microsecond=0).replace(day=now.day+1)
                }
            }
            
            # Update or insert the document
            await collection.update_one(
                {"user_id": state.user_id},
                update_data,
                upsert=True
            )
            
            # Add usage stats to the result
            state.results["usage"] = {
                "prompt_tokens": state.token_usage["prompt"],
                "completion_tokens": state.token_usage["completion"],
                "total_tokens": state.token_usage["total"]
            }
            
        except Exception as e:
            # Log the error but don't fail the response
            state.results["usage_error"] = str(e)
        
        return state
    
    async def run(self, user_id: str, messages: List[Dict[str, str]], query_params: Dict[str, Any]|None = None):
        """Run the workflow with the given inputs."""
        initial_state = GraphState(
            user_id=user_id,
            messages=messages,
            query_params=query_params or {},
            db_client=self.db_client
        )
        
        final_state = await self.workflow.ainvoke(initial_state)
        
        # If there was an error, handle it
        # if final_state.error:
        #     return {
        #         "error": final_state.error,
        #         "usage": final_state.token_usage
        #     }
        
        # return {
        #     "response": final_state.results.get("response"),
        #     "conversation_id": final_state.results.get("conversation_id"),
        #     "usage": final_state.results.get("usage")
        # }
        if final_state["error"]:
            return {
                "error": final_state["error"],
                "usage": final_state["token_usage"]
            }
        
        return {
            "response": final_state['results'].get("response"),
            "conversation_id": final_state["results"].get("conversation_id"),
            "usage": final_state["results"].get("usage")
        }

# ==================== FastAPI Integration ====================

# In your FastAPI app

from fastapi import APIRouter, Depends, HTTPException, Request
from token_limiting import get_user_id, TokenCounter, get_db

# Create a router for the chat endpoints
router = APIRouter()

# Initialize the token counter
token_counter = TokenCounter()

# Create the LangGraph manager instance
graph_manager = None

@router.on_event("startup")
async def startup_event():
    global graph_manager
    db_client = AsyncIOMotorClient("mongodb://localhost:27017")
    graph_manager = LangGraphManager(db_client, token_counter)

@router.post("/chat")
async def chat_endpoint(
    request: Request,
    messages: List[Dict[str, str]],
    user_id: str = Depends(get_user_id),
    db = Depends(get_db)
):
    """Chat endpoint integrated with LangGraph."""
    if not graph_manager:
        raise HTTPException(status_code=500, detail="LangGraph manager not initialized")
    
    result = await graph_manager.run(
        user_id=user_id,
        messages=messages
    )
    
    if "error" in result:
        raise HTTPException(status_code=429, detail=result["error"])
    
    return {
        "id": f"chatcmpl-{uuid4()}",
        "object": "chat.completion",
        "created": int(datetime.now().timestamp()), # int(datetime.utcnow().timestamp()),
        "choices": [
            {
                "index": 0,
                "message": result["response"],
                "finish_reason": "stop"
            }
        ],
        "usage": result["usage"],
        "conversation_id": result["conversation_id"]
    }
