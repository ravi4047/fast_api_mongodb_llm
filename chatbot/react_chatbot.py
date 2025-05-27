import asyncio
from typing import Any, AsyncGenerator, Dict
from langgraph.prebuilt import ToolNode
from langgraph.graph.state import CompiledStateGraph
from mdb.db_manager import DatabaseManager

# https://claude.ai/chat/bd16e0ac-f26c-4874-96da-dfa0b3b534e0

## 👉 Now from that repository object stuff, I also now creating all objects only.(I am not creating it. I am simply from claude only)

## 👉👉👉 Now plan changed. I want to perform real streaming and not fake it with this -> await asyncio.sleep(0.1).
###  Hence, removing this idea to use ------------------------------------ start
# class ReActDatingChatbot:
#     def __init__(self, db_manager: DatabaseManager, openai_api_key: str):
#         self.db = db_manager
#         # openai.api_key = openai_api_key
        
#         # Initialize tools
#         self.tools = [
#             GetMatchesTool(db_manager),
#             AnalyzeProfileTool(db_manager),
#             RelationshipAdviceTool(db_manager)
#         ]
#         self.tool_executor = ToolNode(self.tools) # ToolExecutor(self.tools)
#         self.workflow = self._create_react_workflow()

#     def _create_react_workflow(self) -> CompiledStateGraph:
#         """Create ReAct workflow for intelligent reasoning"""


#     async def process_message_stream(self, user_id: str, message: str) -> AsyncGenerator[Dict[str, Any], None]:
#         """Process message with true streaming using ReAct approach"""
        
#         # Get user context
#         user_profile = await self.db.get_user_profile(user_id)
#         chat_history = await self.db.get_chat_history(user_id, limit=5)
        
#         # Initialize state
#         initial_state = ChatbotState(
#             user_id=user_id,
#             message=message,
#             user_profile=user_profile,
#             potential_matches=[],
#             conversation_history=chat_history,
#             thought="",
#             action="",
#             action_input={},
#             observation="",
#             response="",
#             suggested_matches=[],
#             tools_used=[],
#             reasoning_steps=[]
#         )
        
#         # Stream thinking process
#         yield {
#             "type": "thinking",
#             "content": "Let me think about how to help you...",
#             "step": "reasoning"
#         }
        
#         # Run workflow and stream results
#         try:
#             result = await self.workflow.ainvoke(initial_state)
            
#             # Stream reasoning steps
#             for step in result.get("reasoning_steps", []):
#                 yield {
#                     "type": "reasoning",
#                     "content": step,
#                     "step": "process"
#                 }
#                 await asyncio.sleep(0.1)
            
#             # Stream final response word by word
#             response_words = result["response"].split()
#             accumulated_response = ""
            
#             for i, word in enumerate(response_words):
#                 accumulated_response += word + " "
#                 yield {
#                     "type": "response",
#                     "content": word + " ",
#                     "full_content": accumulated_response.strip(),
#                     "is_final": i == len(response_words) - 1,
#                     "metadata": {
#                         "tools_used": result.get("tools_used", []),
#                         "reasoning_steps": result.get("reasoning_steps", [])
#                     }
#                 }
#                 await asyncio.sleep(0.05)  # Natural typing speed
                
#         except Exception as e:
#             yield {
#                 "type": "error",
#                 "content": f"I encountered an error: {str(e)}",
#                 "is_final": True
#             }

###  Hence, removing this idea to use ------------------------------------ stop