###
### 👉👉 THIS WAS MY FIRST GRAPH TOTALLY HANDMADE AND I REALIZED I DON'T NEED GRAPH AT ALL ############
###

# ## This is developing to make graph for creating bio.
# from typing import TypedDict
# from langgraph.graph import StateGraph, END
# from state import BioGraphState

# ## 👉 I am removing this from here because I don't want circular import.
# # class BioGraphState(TypedDict):
# #     input: str ## This is the instruction from the user about how to create the bio
# #     profile: str


# ## -> One tool needed i.e. fetch profile.
# ## -> No memory needed I guess

# ROUTE_NODE_KEY = "route_node"
# PROCESS_MSSG_NODE_KEY = "process_message_node"
# RUN_NODE_KEY = "run_node"
# GENERATE_RESPONSE_KEY = "generate_response"

# def create_graph():
#     """Create the LangGraph workflow"""
#     # Define the graph
#     workflow = StateGraph(BioGraphState)

#     # Add nodes
#     workflow.add_node(ROUTE_NODE_KEY, route_nodes.route_tool)
#     workflow.add_node(PROCESS_MSSG_NODE_KEY, process_message_node.process_message_tool)
#     workflow.add_node(RUN_NODE_KEY, run_node.run_tool)
#     workflow.add_node(GENERATE_RESPONSE_KEY, generate_response.generate_response)

#     # Add edges
#     workflow.add_edge(ROUTE_NODE_KEY, PROCESS_MSSG_NODE_KEY)
#     workflow.add_edge(PROCESS_MSSG_NODE_KEY, RUN_NODE_KEY)
#     workflow.add_edge(RUN_NODE_KEY, GENERATE_RESPONSE_KEY)
#     workflow.add_edge(GENERATE_RESPONSE_KEY, END)

#     # Set the entry point
#     workflow.set_entry_point(ROUTE_NODE_KEY)

#     # Create memory saver for persistence
#     # memory = MemorySaver()
#     # return workflow.compile(checkpointer=memory)
#     return workflow.compile()
