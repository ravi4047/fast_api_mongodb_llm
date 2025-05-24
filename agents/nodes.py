from typing import Dict, Any, List, Optional
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

from langchain_groq import ChatGroq

from state import ConversationGraphState

from model.graph_entities import EntityExtractionResult, IntentRecognitionResult

# from app.core.graph.base import get_llm, ConversationGraphState
# from app.core.graph.base import IntentRecognitionResult, EntityExtractionResult, Entity
# from app.db.models import USERS_COLLECTION, MESSAGES_COLLECTION, MATCHES_COLLECTION

# Intent Recognition Node
async def intent_recognition_node(state: ConversationGraphState, llm: ChatGroq) -> ConversationGraphState:
    # llm = get_llm()
    
    # Create the intent recognition prompt
    system_prompt = """You are an AI assistant for a dating app. Analyze the user message and determine their intent.
    Focus on identifying if they're asking about:
    1. profile_info_request: Information about another user's profile (age, interests, etc.)
    2. message_info_request: Information about messages or conversations
    3. match_info_request: Information about their matches
    4. personal_task_request: Setting or checking personal tasks/reminders
    5. general_conversation: General conversation or greeting
    
    Respond with ONLY the intent name and confidence score in JSON format.
    """
    
    # Format conversation history context
    context = "Recent conversation:\n"
    for i, msg in enumerate(state.conversation_history[-3:]):
        role = "User" if msg.get("role") == "user" else "Assistant"
        context += f"{role}: {msg.get('content')}\n"
    
    # Current user message
    user_message = f"Current message: {state.current_message}"
    
    # Create messages
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"{context}\n{user_message}\nWhat is the intent of this message?")
    ]
    
    # Get the intent recognition result
    parser = PydanticOutputParser(pydantic_object=IntentRecognitionResult)
    try:
        response = await llm.ainvoke(messages)
        result = parser.parse(response.content.__str__())
        
        # Update state with recognized intent
        return ConversationGraphState(
            **state.model_dump(),
            intent=result.intent
        )
    except Exception as e:
        return ConversationGraphState(
            **state.model_dump(),
            error=f"Intent recognition error: {str(e)}",
            intent="general_conversation"  # Default fallback
        )

# Entity Extraction Node
async def entity_extraction_node(state: ConversationGraphState, llm: ChatGroq) -> ConversationGraphState:
    # llm = get_llm()
    
    # Create the entity extraction prompt
    system_prompt = """You are an AI assistant for a dating app. Extract important entities from the user message.
    Possible entity types:
    - user: Names of users mentioned
    - date: Any date or time references
    - location: Any location references
    - attribute: Profile attributes like "age", "interests", "birthday", etc.
    - match_status: Match-related keywords like "new matches", "unmatched", etc.
    - message_status: Message-related keywords like "unread", "recent", etc.
    
    Respond with ONLY the extracted entities in JSON format.
    """
    
    # Current user message and intent context
    user_message = f"User message: {state.current_message}\nDetected intent: {state.intent}"
    
    # Create messages
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"{user_message}\nWhat entities can you extract?")
    ]
    
    # Get the entity extraction result
    parser = PydanticOutputParser(pydantic_object=EntityExtractionResult)
    try:
        response = await llm.ainvoke(messages)
        result = parser.parse(response.content.__str__())
        
        # Convert entities to dictionary format for easier lookup
        entities_dict = {}
        for entity in result.entities:
            entity_type = entity.type
            if entity_type not in entities_dict:
                entities_dict[entity_type] = []
            entities_dict[entity_type].append({
                "name": entity.name,
                "value": entity.value
            })
        
        # Update state with extracted entities
        return ConversationGraphState(
            **state.model_dump(),
            entities=entities_dict
        )
    except Exception as e:
        return ConversationGraphState(
            **state.model_dump(),
            error=f"Entity extraction error: {str(e)}"
        )

# Routing Node
async def route_by_intent_node(state: ConversationGraphState) -> ConversationGraphState:
    # This node simply passes the state through, as routing is handled
    # by the conditional edges in the graph definition
    return state

# Format Response Node (final node that prepares the response)
async def format_response_node(state: ConversationGraphState) -> ConversationGraphState:
    # If there was an error earlier in the pipeline
    if state.error:
        response = "I'm sorry, I couldn't process your request properly. Could you please try again or rephrase?"
        return ConversationGraphState(
            **state.model_dump(),
            response=response
        )
    
    # If we already have a response from one of the action nodes, use it
    if state.response:
        return state
    
    # Fallback response
    response = "I'm not sure how to help with that. Could you be more specific about what you're looking for?"
    return ConversationGraphState(
        **state.model_dump(),
        response=response
    )