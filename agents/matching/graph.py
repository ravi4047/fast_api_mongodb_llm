# create_matching_subgraph
from langgraph.graph import StateGraph
from typing import Dict, Any, List
import nodes 
from nodes.match_intent_classifier import matching_intent_classifier
from nodes.profile_analyzer import profile_analyzer

## 👉👉 It's useless to call this subgraph.py because every graph is subgraph only.

def create_matching_subgraph():
    # Initialize the matching subgraph
    matching_graph = StateGraph()
    
    # Add all matching-related nodes
    matching_graph.add_node("matching_intent_classifier", matching_intent_classifier)
    matching_graph.add_node("profile_analyzer", profile_analyzer)
    matching_graph.add_node("compatibility_assessor", compatibility_assessor)
    matching_graph.add_node("trustworthiness_evaluator", trustworthiness_evaluator)
    matching_graph.add_node("preference_based_matcher", preference_based_matcher)
    matching_graph.add_node("match_recommender", match_recommender)
    matching_graph.add_node("match_response_generator", match_response_generator)
    
    # Define the flow based on matching intent
    matching_graph.add_edge("matching_intent_classifier", router)
    
    # Set up conditional routing based on matching intent
    matching_graph.add_conditional_edges(
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
    matching_graph.add_edge("compatibility_assessor", "match_response_generator")
    matching_graph.add_edge("trustworthiness_evaluator", "match_response_generator")
    matching_graph.add_edge("preference_based_matcher", "match_recommender")
    matching_graph.add_edge("match_recommender", "match_response_generator")
    matching_graph.add_edge("profile_analyzer", "match_response_generator")
    
    # Compile the subgraph
    return matching_graph.compile()

# Router function for matching intents
def route_by_matching_intent(state: Dict[str, Any]) -> str:
    intent = state.get("matching_intent", "")
    
    if "compatibility" in intent:
        return "assess_compatibility"
    elif "trustworthiness" in intent or "trust" in intent:
        return "evaluate_trustworthiness"
    elif "recommendation" in intent or "suggest" in intent or "find" in intent:
        return "find_recommendations"
    elif "profile" in intent or "analyze" in intent:
        return "analyze_profile"
    else:
        return "default"