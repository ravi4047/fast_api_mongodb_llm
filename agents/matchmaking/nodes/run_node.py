import json
from state import AgentState

async def run_tool(state: AgentState) -> AgentState:
    """Run the selected tool."""
    tool_name = state["tool_name"]
    tool_input = state["tool_input"]
    
    tool = TOOLS.get(tool_name)
    if not tool:
        state["tool_result"] = json.dumps({"success": False, "message": f"Tool {tool_name} not found."})
        return state
    
    try:
        result = await tool(tool_input)
        state["tool_result"] = result
    except Exception as e:
        state["tool_result"] = json.dumps({"success": False, "message": f"Error running tool: {str(e)}"})
    
    return state
