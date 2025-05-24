from fastapi import Depends
from llm.llm import AI_Engine, get_ai_engine
from mdb.profile import search_profile_by_name
from state import AgentState
from langchain_core.messages import HumanMessage, SystemMessage
from prompts import MESSAGE_EVALUATION_PROMPT
import json

# https://claude.ai/chat/3189db2e-a00b-489b-8118-b1a5d97f8dc5
async def process_message_tool(state: AgentState, ai_engine: AI_Engine = Depends(get_ai_engine)) -> AgentState:
    """Process the message sending tool with additional steps."""
    if state["tool_name"] != "send_message":
        return state
    
    # This I have coded.
    if state["tool_input"] is None:
        raise
    
    user_message = state["tool_input"].get("message", "")
    user_id = state["tool_input"].get("user_id", "")

    # We need to determine the recipient and extract the actual message
    # This requires more complex analysis

    # ai_engine = get_ai_engine()

    extraction_result = await ai_engine.llm.ainvoke(user_message)
    extraction_content = extraction_result.content.__str__()

    # Parse the extraction result
    # Expected format: Recipient: <name>, Message: <message>
    recipient_name = ""  ## 👉👉 I don't think simply using recipient name is good.
    message_content = ""

    try:
        if "recipient:" in extraction_content.lower():
            parts = extraction_content.split("Message:", 1)
            recipient_part = parts[0]
            message_content = parts[1].strip() if len(parts) > 1 else ""

            # Extract recipient name
            recipient_name = recipient_part.split("Recipient:",1)[1].strip()
        else:
            # Fallback
            state["tool_name"] = "default_response"
            state["tool_input"] = {"user_id": user_id, "message": "I couldn't identify who you want to send a message to. Could you please specify the recipient's name clearly?"}
            return state
    except:
        state["tool_name"] = "default_response"
        state["tool_input"] = {"user_id": user_id, "message": "I couldn't process your message request correctly. Please try again with a clearer format like 'Tell Sarah that I enjoyed our conversation.'"}
        return state

    # Now we need to check if this is an appropriate message to send
    evaluation_prompt = [
        SystemMessage(content=MESSAGE_EVALUATION_PROMPT),
        HumanMessage(content=message_content)
    ]
    
    evaluation_result = await ai_engine.llm.ainvoke(evaluation_prompt)
    evaluation = evaluation_result.content

    if "INAPPROPRIATE" in evaluation:
        state["tool_name"] = "default_response"
        state["tool_input"] = {
            "user_id": user_id,
            "message": "I can't send that message as it contains inappropriate content. Could you rephrase your message in a more respectful way?"
        }
        return state
    
    if "REVISED" in evaluation:
        state["tool_name"] = "default_response"
        state["tool_input"] = {
            "user_id": user_id,
            "message": "I can't send that message as it contains inappropriate content. Could you rephrase your message in a more respectful way?"
        }
        return state
    
    # Now we need to get the recipient's user ID
    # In a real app, we would search the database for the user
    # For simplicity, we'll assume we have a tool for this
    # Here we'll use the profile search tool
    profiles_json = await search_profile_by_name(name=recipient_name, user_id=user_id)
    profiles_data = json.loads(profiles_json)
    
    if not profiles_data.get("success", False) or profiles_data.get("count", 0) == 0:
        state["tool_name"] = "default_response"
        state["tool_input"] = {"user_id": user_id, "message": f"I couldn't find a user named '{recipient_name}'. Please check the name and try again."}
        return state
    
    # Get the first profile
    recipient_profile = profiles_data["profiles"][0]
    recipient_id = recipient_profile["id"]
    
    # Update the tool input
    state["tool_input"] = {
        "from_user_id": user_id,
        "to_user_id": recipient_id,
        "message": message_content
    }
    
    return state