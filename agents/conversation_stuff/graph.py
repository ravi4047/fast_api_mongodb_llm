from langchain.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.checkpoint.mongodb import MongoDBSaver

def route_by_conversation():
        
    pass

def create_conversation_graph():
    conversation_graph = StateGraph()

    # Add all conversation related nodes
    conversation_graph.add_node("uuuuuuu", uuuu)
    conversation_graph.add_node("ssssss", ssss)
    conversation_graph.add_node("", )

    conversation_graph.add_conditional_edges(
        "conversation",
        route_by_conversation,
        {
            "": "",
            "": "",
            "": ""
        }
    )

    return conversation_graph.compile()