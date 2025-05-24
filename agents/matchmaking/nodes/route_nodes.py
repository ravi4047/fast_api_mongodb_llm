from fastapi import Depends
from state import AgentState
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from utils.content_filtering_utility import is_message_appropriate

from prompts import ROUTER_PROMPT

from llm.llm import AI_Engine, get_ai_engine

# https://claude.ai/chat/3189db2e-a00b-489b-8118-b1a5d97f8dc5
# Node functions

async def route_tool(state: AgentState)-> AgentState:
    """Route to the appropriate node based on the user input"""
    messages = state['messages']
    user_id = state['user_id']

    # Extract the latest user message
    last_user_message = next((msg for msg in reversed(messages) 
                             if isinstance(msg, HumanMessage)), None)
    
    if not last_user_message:
        return state
    
    user_message = last_user_message.content.__str__()

    # Check if the message is appropriate
    is_appropriate, sanitized_message = is_message_appropriate(user_message)

    if not is_appropriate:
        # If the message is inappropriate, return a default response explaining the issue
        state["tool_name"] = "default_response"
        state["tool_input"] = {
            "user_id": user_id,
            "message": "I noticed your message contains content that may be inappropriate. As your dating assistant, I'm here to help you find meaningful connections through respectful interactions. Can I help you with something else?"
        }
        return state
    
    # Prompt for the router
    # router_prompt = ChatPromptTemplate.from_messages([
    router_prompt = [
        SystemMessage(content=ROUTER_PROMPT),
        # HumanMessage(content=user_message)
        HumanMessage(content=sanitized_message)
    ]
    # router_prompt.

    # ai_engine = get_ai_engine()

    # Get the tool name
    tool_name = await ai_engine.llm.ainvoke(router_prompt)
    tool_name = tool_name.content.__str__().strip().lower()

    # Extract the tool name from the response if necessary
    if "search_profile_by_name" in tool_name:
        tool_name = "search_profile_by_name"
        state["tool_input"] = {"name": user_message, "user_id": user_id}
    elif "get_feed_history" in tool_name:
        tool_name = "get_feed_history"
        state["tool_input"] = {"user_id": user_id, "limit": 10}

        ## 👉 The AI didn't understand here. I want to do few shot prompting here. That why are you trying to send the data
    # elif "get_user_matches" in tool_name:
    #     tool_name = "get_user_matches"
        # state["tool_input"] = {"user_id": user_id}

    elif "send_message" in tool_name:
        tool_name = "send_message"
        # For message sending, we need more processing in the next step
        state["tool_input"] = {"message": user_message, "user_id": user_id}
    else:
        tool_name = "default_response"
        state["tool_input"] = {"user_id": user_id, "message": user_message}
    
    state["tool_name"] = tool_name
    return state