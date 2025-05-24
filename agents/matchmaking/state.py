from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from typing import TypedDict, List, Union, Optional, Dict, Any


# Define state
class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage, SystemMessage]]
    tool_name: Optional[str]
    tool_input: Optional[Dict[str, Any]]
    tool_result: Optional[str]
    user_id: str

##