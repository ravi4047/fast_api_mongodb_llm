from langchain.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.checkpoint.mongodb import MongoDBSaver

def create_general_questions_graph():
    # Initialize the matching subgraph
    general_questions_graph = StateGraph()
    
    # Add all personal info nodes
    general_questions_graph.add_node("matching_intent_classifier", matching_intent_classifier)
    general_questions_graph.add_node("profile_analyzer", profile_analyzer)
    general_questions_graph.add_node("compatibility_assessor", compatibility_assessor)
    general_questions_graph.add_node("trustworthiness_evaluator", trustworthiness_evaluator)
    general_questions_graph.add_node("preference_based_matcher", preference_based_matcher)
    general_questions_graph.add_node("match_recommender", match_recommender)
    general_questions_graph.add_node("match_response_generator", match_response_generator)
    
    # Define the flow based on matching intent
    general_questions_graph.add_edge("matching_intent_classifier", router)
    
    # Set up conditional routing based on matching intent
    general_questions_graph.add_conditional_edges(
        "matching_intent_classifier",
        route_by_matching_intent,
        {
            "assess_compatibility": "compatibility_assessor",
            "evaluate_trustworthiness": "trustworthiness_evaluator",
            "find_recommendations": "preference_based_matcher",
            "analyze_profile": "profile_analyzer",
            "default": "match_response_generator"
        }
    )
    
    # Connect all processing nodes to the response generator
    general_questions_graph.add_edge("compatibility_assessor", "match_response_generator")
    general_questions_graph.add_edge("trustworthiness_evaluator", "match_response_generator")
    general_questions_graph.add_edge("preference_based_matcher", "match_recommender")
    general_questions_graph.add_edge("match_recommender", "match_response_generator")
    general_questions_graph.add_edge("profile_analyzer", "match_response_generator")

    general_questions_graph.add_node("", )
    
    # Compile the subgraph
    return general_questions_graph.compile()