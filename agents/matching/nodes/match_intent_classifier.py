from fastapi import Depends
from langchain_groq import ChatGroq
from typing import Dict, Any
from mdb.setup import mongodb_dependency, Mongo_Setup, get_mongodb

def matching_intent_classifier(state: Dict[str, Any], mdb: Mongo_Setup = Depends(get_mongodb) ) -> Dict[str, Any]:
    user_query = state["user_query"]
    
    # Use LLM to classify the matching-specific intent
    matching_intent = llm.invoke( 
        f"Classify this dating app matching query: '{user_query}' into one of these categories: "
        "'assess_compatibility', 'evaluate_trustworthiness', 'find_recommendations', "
        "'analyze_profile', or 'general_matching_question'. Respond with just the category name."
    )
    
    state["matching_intent"] = matching_intent.__str__().strip().lower()

    return state