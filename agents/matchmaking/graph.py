from state import AgentState
from langgraph.graph import StateGraph, END
from nodes import route_nodes, process_message_node, run_node, generate_response
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from typing import List, Any, Dict

from langgraph.checkpoint.memory import MemorySaver

from prompts import SYSTEM_PROMPT

ROUTE_NODE_KEY = "route_node"
PROCESS_MSSG_NODE_KEY = "process_message_node"
RUN_NODE_KEY = "run_node"
GENERATE_RESPONSE_KEY = "generate_response"

def create_graph():
    """Create the LangGraph workflow"""
    # Define the graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node(ROUTE_NODE_KEY, route_nodes.route_tool)
    workflow.add_node(PROCESS_MSSG_NODE_KEY, process_message_node.process_message_tool)
    workflow.add_node(RUN_NODE_KEY, run_node.run_tool)
    workflow.add_node(GENERATE_RESPONSE_KEY, generate_response.generate_response)

    # Add edges
    workflow.add_edge(ROUTE_NODE_KEY, PROCESS_MSSG_NODE_KEY)
    workflow.add_edge(PROCESS_MSSG_NODE_KEY, RUN_NODE_KEY)
    workflow.add_edge(RUN_NODE_KEY, GENERATE_RESPONSE_KEY)
    workflow.add_edge(GENERATE_RESPONSE_KEY, END)

    # Set the entry point
    workflow.set_entry_point(ROUTE_NODE_KEY)

    # Create memory saver for persistence
    memory = MemorySaver()

    return workflow.compile(checkpointer=memory)

## Main function to process a message
async def process_message(user_id: str, message: str, history: List[Dict[str, Any]] = []) -> str:
    """
    Process a user message and return a response.
    
    Args:
        user_id: The ID of the user
        message: The message from the user
        history: Optional chat history
        
    Returns:
        The response from the agent
    """
    # Convert history to message format
    messages: list[BaseMessage] = [SystemMessage(content=SYSTEM_PROMPT)]
    
    if history:
        for entry in history:
            if entry.get("is_user", False):
                messages.append(HumanMessage(content=entry["message"]))
            else:
                messages.append(AIMessage(content=entry["message"]))
    
    # Add the current message
    messages.append(HumanMessage(content=message))
    
    # Create the initial state
    state = {
        "messages": messages,
        "tool_name": None,
        "tool_input": None,
        "tool_result": None,
        "user_id": user_id
    }
    
    # Check if we have a saved state for this user
    checkpoint_id = f"user_{user_id}"
    
    try:
        # Initialize the agent
        graph = create_graph()

        # Run the graph
        result = await graph.ainvoke(state)
        
        # # Save the state
        # memory(checkpoint_id, result)
        
        # Get the last AI message
        last_message = next((msg for msg in reversed(result["messages"]) 
                           if isinstance(msg, AIMessage)), None)
        
        if last_message:
            return last_message.content.__str__()
        else:
            return "I'm sorry, I wasn't able to generate a response. Please try again."
            
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        return "I'm sorry, there was an error processing your message. Please try again."