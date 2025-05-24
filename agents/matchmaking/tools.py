from typing import Dict, List, Any, Callable, Optional, TypedDict
from pydantic import BaseModel, Field
import json

from utils.content_filtering_utility import is_message_appropriate
from langchain_core.tools import tool

from repository.chat_repository import chat_repo
from repository.match_repository import match_repo
from repository.profile_repository import profile_repo
from repository.feed_repository import feed_history_repo
from repository.message_repository import message_repo

class ProfileSearchParams(BaseModel):
    """Parameters for profile search."""
    name: str = Field(description="Name of the person to search for")
    user_id: str = Field(description="ID of the user making the search")

class FeedHistoryParams(BaseModel):
    """Parameters for getting feed history."""
    user_id: str = Field(description="ID of the user")
    limit: int = Field(default=10, description="Maximum number of profiles to return")

class MatchesParams(BaseModel):
    """Parameters for getting user matches."""
    user_id: str = Field(description="ID of the user")

class MessageParams(BaseModel):
    """Parameters for sending a message."""
    from_user_id: str = Field(description="ID of the user sending the message")
    to_user_id: str = Field(description="ID of the user receiving the message")
    message: str = Field(description="Content of the message")

class DefaultResponseParams(BaseModel):
    """Parameters for default response."""
    user_id: str = Field(description="ID of the user")
    message: str = Field(description="User's message")

## 🤔🤔🤔 Considering the Repository way as a recommended approach, how will I use this tool stuff.

@tool
async def search_profile_by_name(params: ProfileSearchParams) -> str:
    """
    Search for a user profile by name.
    """
    # profiles = await profile.get_profile_by_name(params.name)
    profiles = await profile_repo.search_by_name(params.name)
    
    if not profiles:
        return json.dumps({
            "success": False,
            "message": f"No profiles found with the name '{params.name}'."
        })
    
    # Format profiles for display
    formatted_profiles = []
    for profile in profiles:
        formatted_profiles.append({
            "id": profile["_id"],
            "name": profile["name"],
            "age": profile["age"],
            "bio": profile["bio"],
            "interests": profile["interests"],
            "photos": profile["photos"][0] if profile["photos"] else None
        })
    
    return json.dumps({
        "success": True,
        "profiles": formatted_profiles,
        "count": len(formatted_profiles)
    })

@tool
async def get_feed_history(params: FeedHistoryParams) -> str:
    """
    Get the user's feed history - profiles they've been shown previously.
    """
    feed_history = await feed_history_repo.get_feed_history(params.user_id, params.limit)
    
    if not feed_history:
        return json.dumps({
            "success": False,
            "message": "No feed history found."
        })
    
    # Get full profile details for each profile in feed history
    profiles = []
    for entry in feed_history:
        profile = await profile_repo.get_profile_by_id(entry["profile_id"])
        if profile:
            profiles.append({
                "id": profile["_id"],
                "name": profile["name"],
                "age": profile["age"],
                "bio": profile["bio"],
                "interests": profile["interests"],
                "photos": profile["photos"][0] if profile["photos"] else None,
                "viewed_at": entry["timestamp"].isoformat()
            })
    
    return json.dumps({
        "success": True,
        "profiles": profiles,
        "count": len(profiles)
    })

@tool
async def get_user_matches(params: MatchesParams) -> str:
    """
    Get the user's current matches.
    """
    # matches = await get_user_matches(params.user_id)
    matches = await match_repo.get_user_matches(params.user_id)
    
    if not matches:
        return json.dumps({
            "success": False,
            "message": "No matches found."
        })
    
    # Get full profile details for each match
    matched_profiles = []
    for match in matches:
        # Determine the ID of the other user in the match
        other_user_id = match["user2_id"] if match["user1_id"] == params.user_id else match["user1_id"]
        profile = await profile_repo.get_profile_by_id(other_user_id)
        
        if profile:
            matched_profiles.append({
                "id": profile["_id"],
                "name": profile["name"],
                "age": profile["age"],
                "bio": profile["bio"],
                "interests": profile["interests"],
                "photos": profile["photos"][0] if profile["photos"] else None,
                "matched_at": match["created_at"].isoformat()
            })
    
    return json.dumps({
        "success": True,
        "matches": matched_profiles,
        "count": len(matched_profiles)
    })

@tool
async def send_message(params: MessageParams) -> str:
    """
    Send a message from one user to another.
    """
    # Check if the message is appropriate
    is_appropriate, sanitized_message = is_message_appropriate(params.message)
    
    if not is_appropriate:
        return json.dumps({
            "success": False,
            "message": "The message contains inappropriate content and cannot be sent."
        })
    
    # Send the sanitized message
    message_id = await message_repo.add_message(params.from_user_id, params.to_user_id, sanitized_message)
    
    return json.dumps({
        "success": True,
        "message": "Message sent successfully.",
        "message_id": message_id
    })

@tool
async def default_response(params: DefaultResponseParams) -> str:
    """
    Provide a default response when no specific tool action is needed.
    """
    # This function doesn't need to do anything special - it's a fallback
    # The LLM will generate an appropriate response based on the user's message
    return json.dumps({
        "success": True,
        "message": params.message,
        "requires_llm_response": True
    })