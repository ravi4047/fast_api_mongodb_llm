from fastapi import FastAPI, Depends
from state import AgentState
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
import json
from prompts import PROFILE_DESCRIPTION_PROMPT, SYSTEM_PROMPT
from llm.llm import get_ai_engine

async def generate_response(state: AgentState, ai_engine = Depends(get_ai_engine)) -> AgentState:
    """Generate a response based on the tool result."""
    messages = state["messages"]
    tool_result = state["tool_result"] 
    user_id = state["user_id"]
    
    try:
        if tool_result is None:
            raise
        result_data = json.loads(tool_result)
    except:
        result_data = {"success": False, "message": "Failed to parse tool result."}
    
    # Different handling based on the tool
    if state["tool_name"] == "search_profile_by_name" and result_data.get("success", False):
        profiles = result_data.get("profiles", [])
        
        if profiles:
            # profile_prompt = ChatPromptTemplate.from_messages([
            profile_prompt = [
                SystemMessage(content=PROFILE_DESCRIPTION_PROMPT),
                HumanMessage(content=json.dumps(profiles[0]))
            ]
            
            profile_description = await ai_engine.llm.ainvoke(profile_prompt)
            
            response_prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content=SYSTEM_PROMPT),
                MessagesPlaceholder(variable_name="history"),
                SystemMessage(content=f"Profile information: {profile_description.content}\n\nRespond to the user's request about this profile, offering to show more details if needed."),
            ])
            
            # Generate response
            response = await ai_engine.conversational_llm.ainvoke(
                response_prompt.format(history=messages)
            )
            messages.append(response)
    
    elif state["tool_name"] == "get_feed_history" and result_data.get("success", False):
        profiles = result_data.get("profiles", [])
        
        if profiles:
            # Create a summary of the feed history
            feed_summary = "\n".join([
                f"{i+1}. {profile['name']}, {profile['age']} - {profile['bio'][:50]}..."
                for i, profile in enumerate(profiles[:5])
            ])
            
            response_prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content=SYSTEM_PROMPT),
                MessagesPlaceholder(variable_name="history"),
                SystemMessage(content=f"Feed history summary:\n{feed_summary}\n\nRespond to the user's request about their previous feed, mentioning that these were profiles they've seen recently."),
            ])
            
            # Generate response
            response = await ai_engine.conversational_llm.ainvoke(
                response_prompt.format(history=messages)
            )
            messages.append(response)
    
    elif state["tool_name"] == "get_user_matches" and result_data.get("success", False):
        matches = result_data.get("matches", [])
        
        if matches:
            # Create a summary of the matches
            matches_summary = "\n".join([
                f"{i+1}. {match['name']}, {match['age']} - {match['bio'][:50]}..."
                for i, match in enumerate(matches[:5])
            ])
            
            response_prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content=SYSTEM_PROMPT),
                MessagesPlaceholder(variable_name="history"),
                SystemMessage(content=f"Matches summary:\n{matches_summary}\n\nRespond to the user's request about their matches, congratulating them on their connections."),
            ])
            
            # Generate response
            response = await ai_engine.conversational_llm.ainvoke(
                response_prompt.format(history=messages)
            )
            messages.append(response)
    
    elif state["tool_name"] == "send_message" and result_data.get("success", False):
        response_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="history"),
            SystemMessage(content="The message has been sent successfully. Confirm to the user that their message was delivered."),
        ])
        
        # Generate response
        response = await ai_engine.conversational_llm.ainvoke(
            response_prompt.format(history=messages)
        )
        messages.append(response)
    
    else:
        # Default response
        response_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="history"),
        ])
        
        # Generate response
        response = await ai_engine.conversational_llm.ainvoke(
            response_prompt.format(history=messages)
        )
        messages.append(response)
    
    return state
