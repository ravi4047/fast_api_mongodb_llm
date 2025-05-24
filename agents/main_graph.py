## Perplexity stuff 
from fastapi import FastAPI, Depends
from langgraph.graph import StateGraph

from matching.graph import create_matching_subgraph
from personal_info.graph import create_personal_info_subgraph
from conversation_stuff.graph import create_conversation_graph
from general_questions_stuff.graph import create_general_questions_graph

from llm.llm import get_ai_engine # ai_engine

MATCHING_INFO_HANDLER = "matching_info_handler"
PERSONAL_INFO_HANDLER = "personal_info_handler"
CONVERSATION_HANDLER = "personal_info_handler"
GENERAL_QUESTIONS_HANDLER = "general_questions_handler"

def domain_classifier(state, ai_engine = Depends(get_ai_engine)):
    user_query = state["user_query"]
    
    # Use LLM to classify the query into the appropriate domain
    llm = ai_engine.llm
    domain = llm.invoke(
        f"Classify this dating app query: '{user_query}' into one of these domains: "
        "'personal_info', 'conversation_topics', 'general_questions', 'matching'"
    )
    
    # Update state with the identified domain
    state["identified_domain"] = domain.strip().lower()
    return state

def domain_router(state):
    domain = state["identified_domain"]
    
    if "matching" in domain:
        # return "matching_info_handler"
        return MATCHING_INFO_HANDLER
    elif "personal_info" in domain:
        # return "personal_info_handler"
        return PERSONAL_INFO_HANDLER
    elif "conversation" in domain:
        # return "conversation_handler"
        return CONVERSATION_HANDLER
    else:
        # return "general_questions_handler"
        return GENERAL_QUESTIONS_HANDLER


# Domain-specific collections
domain_collections = {
    "users": db.users,                       # Core user profiles
    "matching": db.matching_preferences,     # Matching criteria and history
    "conversations": db.conversation_topics, # Conversation preferences and history
    "general": db.general_questions          # General Q&A tracking
}

# Domain-Specific Intent Recognition
# Each domain will have its own set of intents that need to be recognized:

def matching_intent_recognizer(state, ai_engine = Depends(get_ai_engine)):
    user_query = state["user_query"]
    
    # Use LLM to identify matching-specific intent
    matching_intent = ai_engine.llm.invoke(
        f"Identify the matching-related intent in this query: '{user_query}'. "
        "Choose from: 'assess_compatibility', 'find_recommendations', "
        "'evaluate_trustworthiness', 'profile_preferences', 'other'"
    )
    
    state["matching_intent"] = matching_intent.strip().lower()
    return state

# Cross-Domain Information Sharing
# Enable information sharing between domains when necessary:
def cross_domain_information_retrieval(state):
    current_domain = state["identified_domain"]
    user_id = state["user_id"]
    
    # Retrieve relevant information from other domains
    if current_domain == "matching":
        # Get personal info that might be relevant for matching
        personal_info = db.personal_info.find_one({"user_id": user_id})
        if personal_info:
            state["relevant_personal_info"] = personal_info
    
    return state

def setup_main_graph_setup():
    # Create the main graph
    main_graph = StateGraph()

    # Add domain classification and routing nodes
    main_graph.add_node("domain_classifier", domain_classifier)
    main_graph.add_node("domain_router", domain_router)

    # Create domain-specific subgraphs
    matching_graph = create_matching_subgraph()
    personal_info_graph = create_personal_info_subgraph()
    conversation_graph = create_conversation_graph()
    general_questions_graph = create_general_questions_graph()

    # Add subgraphs to main graph

    ## 👉 Dude there is no method add_subgraph. How does they made that? 

    # main_graph.add_subgraph("matching_subgraph", matching_graph)
    # main_graph.add_subgraph("personal_info_subgraph", personal_info_graph)
    # main_graph.add_subgraph("conversation_subgraph", conversation_graph)
    # main_graph.add_subgraph("general_questions_subgraph", general_questions_graph)
    main_graph.add_node(MATCHING_INFO_HANDLER, matching_graph)
    main_graph.add_node(PERSONAL_INFO_HANDLER, personal_info_graph)
    main_graph.add_node(CONVERSATION_HANDLER, conversation_graph)
    main_graph.add_node(GENERAL_QUESTIONS_HANDLER, general_questions_graph)

    # Define the flow
    main_graph.add_edge("start", "domain_classifier")
    main_graph.add_edge("domain_classifier", "domain_router")
    # main_graph.add_edge("domain_router", ["matching_subgraph", "personal_info_subgraph", 
    #                                     "conversation_subgraph", "general_questions_subgraph"])
    main_graph.add_conditional_edges("domain_router", domain_router)

    # All subgraphs return to a response formatter
    for subgraph in ["matching_subgraph", "personal_info_subgraph", 
                    "conversation_subgraph", "general_questions_subgraph"]:
        main_graph.add_edge(subgraph, "format_response")

    # Compile the graph
    main_graph_instance = main_graph.compile()
