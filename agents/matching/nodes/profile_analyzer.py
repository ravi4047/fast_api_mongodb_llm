from fastapi import Depends
from langchain_groq import ChatGroq
from typing import Dict, Any
from mdb.setup import mongodb_dependency, Mongo_Setup, get_mongodb
from llm.llm import LLM_Setup, get_llm

def profile_analyzer(
        state: Dict[str, Any], 
        # llm: ChatGroq, 
        # llm: ChatGroq = 
        llm: LLM_Setup = Depends(get_llm),
        mdb: Mongo_Setup = Depends(get_mongodb)) -> Dict[str, Any]:
    user_query = state["user_query"]
    
    # Extract profile ID from query if present, otherwise use target_id
    profile_id = state.get("target_id")
    if not profile_id:
        # Use NLP to extract profile identifier from query
        extraction_result = llm.invoke(
            f"Extract any profile identifier (name, username, ID) from this query: '{user_query}'"
        )
        profile_id = extraction_result.strip()

    profile_data = mdb.get_users_collection().find_one()
    
    # Retrieve profile from MongoDB
    profile_data = db.users.find_one({"$or": [
        {"_id": profile_id},
        {"username": profile_id},
        {"name": profile_id}
    ]})
    
    if not profile_data:
        state["profile_analysis"] = "Profile not found. Please check the name or ID and try again."
        return state
    
    # Analyze profile with LLM
    profile_analysis = llm.invoke(
        f"Analyze this dating profile objectively: {profile_data}. "
        "Highlight key personality traits, interests, communication style, and potential compatibility factors."
    )
    
    state["profile_data"] = profile_data
    state["profile_analysis"] = profile_analysis
    return state

# hi = profile_analyzer({}, ChatGroq())