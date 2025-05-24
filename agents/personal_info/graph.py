# create_matching_subgraph
from langgraph.graph import StateGraph
from typing import Dict, Any, List

def create_personal_info_subgraph():
    # Initialize the matching subgraph
    personal_info_graph = StateGraph()
    
    # Add all personal info nodes
    personal_info_graph.add_node("matching_intent_classifier", matching_intent_classifier)
    personal_info_graph.add_node("profile_analyzer", profile_analyzer)
    personal_info_graph.add_node("compatibility_assessor", compatibility_assessor)
    personal_info_graph.add_node("trustworthiness_evaluator", trustworthiness_evaluator)
    personal_info_graph.add_node("preference_based_matcher", preference_based_matcher)
    personal_info_graph.add_node("match_recommender", match_recommender)
    personal_info_graph.add_node("match_response_generator", match_response_generator)
    
    # Define the flow based on matching intent
    personal_info_graph.add_edge("matching_intent_classifier", router)
    
    # Set up conditional routing based on matching intent
    personal_info_graph.add_conditional_edges(
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
    personal_info_graph.add_edge("compatibility_assessor", "match_response_generator")
    personal_info_graph.add_edge("trustworthiness_evaluator", "match_response_generator")
    personal_info_graph.add_edge("preference_based_matcher", "match_recommender")
    personal_info_graph.add_edge("match_recommender", "match_response_generator")
    personal_info_graph.add_edge("profile_analyzer", "match_response_generator")
    
    # Compile the subgraph
    return personal_info_graph.compile()