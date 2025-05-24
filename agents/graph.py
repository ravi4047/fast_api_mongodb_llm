from langchain.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain.chat_models.base import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.checkpoint.mongodb import MongoDBSaver

from pymongo.database import Database

from nodes import intent_recognition_node, entity_extraction_node, route_by_intent_node, format_response_node
from action_nodes import personal_task_action_node, general_conversation_node

# from tools.personal_info_about_user import get_user_birthday

from pymongo.collection import Collection

from typing import Optional

from langchain_groq import ChatGroq
from state import ConversationGraphState
## Define a tool nodes

# @tool
# def get_info_about_mongodb(user_query:str)->str:
    # pass

## Do you need the tool. I don't think so. It's the manual understanding that we will use the previous stuff.

class GraphState(TypedDict):
    messages: list[BaseMessage] # Actually I will be saving it inside the mongodb.
    input:str
    retrieved_info: Optional[str]


# Nodes -----------
## 👉👉 We are not building the chains. So just invoke it. Because it's nodes.

# >> I finally understood to include the setup of LLM in the graph.py and write it down separately and include it in the lifespan.
# Thanks for the wrapper idea.
# https://chatgpt.com/c/681f72e4-5ad0-800d-b706-dc2453ab111e
def prompt_node(state: GraphState, llm: BaseChatModel)->GraphState:
    messages = state.get("messages", [])

    human = HumanMessage(content=state["input"])

    # LLM Interaction
    response = llm.invoke(messages+[human])

    # Update state
    messages.extend([human, response])

    # return {messages: messages, "input": ""} ## Now too much strictness.
    return GraphState(messages=messages, input="", retrieved_info=None)

graph = StateGraph(GraphState)

@tool
def my_mongodb_tool(user_query:str)->str:
    return ""

## 
def build_graph(llm: BaseChatModel, memory: MongoDBSaver, db: Database): # userCollection: Collection):

    tool_node = ToolNode([my_mongodb_tool])

    def prompt_node_wrapper(state: GraphState):
        return prompt_node(state, llm)
    
    # def mongo_wrapper(playerName: str, uid: str, state: GraphState, playerCollection:Collection):
    #     return get_user_birthday(playerName=playerName, uid=uid, playerCollection=userCollection, state=state)

    graph.add_node("prompt_node", prompt_node_wrapper)
    graph.add_node("tools", tool_node)

    graph.add_edge("START", "prompt_node")
    graph.add_edge("tools", "prompt_node")
    graph.add_conditional_edges(
        "prompt_node",
        tools_condition, 
        {"tools": "tools", "END": END})
    # graph.add_edge("tool_node", tool) ## You don't need to explicitly tell th

    #Setting checkpointer https://www.mongodb.com/docs/atlas/atlas-vector-search/ai-integrations/langgraph/?msockid=1646517fdc136697037643c0dd1567a1#usage-1
    
    ## 🤔🤔 Why do you need checkpointer but?
    graph.compile(checkpointer=memory)



#### ---------------=======================================----------------------------=-=-=-==---=



# # Intent recognition schema
# class IntentRecognitionResult(BaseModel):
#     intent: str = Field(description="The detected intent of the user message")
#     confidence: float = Field(description="Confidence score between 0 and 1")
    
#     class Config:
#         schema_extra = {
#             "examples": [
#                 {
#                     "intent": "profile_info_request",
#                     "confidence": 0.92
#                 }
#             ]
#         }

# # Entity extraction schema
# class Entity(BaseModel):
#     name: str = Field(description="Name of the extracted entity")
#     value: str = Field(description="Value of the extracted entity")
#     type: str = Field(description="Type of entity (user, date, location, etc.)")

# class EntityExtractionResult(BaseModel):
#     entities: List[Entity] = Field(description="List of extracted entities")

# Create the base state graph
def create_conversation_graph(llm: ChatGroq) -> StateGraph:
    # Initialize the graph
    graph = StateGraph(GraphState)

    def intent_recognition_node_wrapper(state: ConversationGraphState):
        return intent_recognition_node(state, llm)
    
    # Define the nodes
    # graph.add_node("intent_recognition", intent_recognition_node)
    graph.add_node("intent_recognition", intent_recognition_node_wrapper)

    def entity_extraction_node_wrapper(state: ConversationGraphState):
        return intent_recognition_node(state, llm)

    graph.add_node("entity_extraction", entity_extraction_node_wrapper)

    graph.add_node("route_by_intent", route_by_intent_node)
    
    # Intent-specific action nodes
    graph.add_node("profile_info_action", profile_info_action_node)
    graph.add_node("message_info_action", message_info_action_node)
    graph.add_node("match_info_action", match_info_action_node)
    # I think you have missed add_node profile_info_action_node, message_info_action_node, match_info_action_node nodes.

    def personal_task_action_node_wrapper(state: ConversationGraphState):
        return personal_task_action_node(state, llm)
    graph.add_node("personal_task_action", personal_task_action_node_wrapper)

    def general_conversation_node_wrapper(state: ConversationGraphState):
        return general_conversation_node(state, llm)
    graph.add_node("general_conversation", general_conversation_node_wrapper)

    graph.add_node("format_response", format_response_node)
    
    # Define the edges
    graph.add_edge("intent_recognition", "entity_extraction")
    graph.add_edge("entity_extraction", "route_by_intent")
    
    # Intent routing edges
    graph.add_conditional_edges(
        "route_by_intent",
        lambda state: state.intent,
        {
            "profile_info_request": "profile_info_action",
            "message_info_request": "message_info_action",
            "match_info_request": "match_info_action",
            "personal_task_request": "personal_task_action",
            "general_conversation": "general_conversation",
        },
        # default_edge="general_conversation"
    )
    
    # Connect all action nodes to format_response
    graph.add_edge("profile_info_action", "format_response")
    graph.add_edge("message_info_action", "format_response")
    graph.add_edge("match_info_action", "format_response")
    graph.add_edge("personal_task_action", "format_response")
    graph.add_edge("general_conversation", "format_response")
    
    # Final edge to end
    graph.add_edge("format_response", END)
    
    # Set the entry point
    graph.set_entry_point("intent_recognition")
    
    return graph