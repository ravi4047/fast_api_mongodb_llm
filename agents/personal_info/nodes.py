from pymongo.collection import Collection
from agent.graph import GraphState
from mdb.user import get_user
"""
Multiple nodes related to personal info.
"""

## 👉👉 It's useless to call this subgraph.py because every graph is subgraph only.

# This runs after personal info node.
def fetch_personal_info_node(uid:str, state:dict, userCollection: Collection)->GraphState:
    # Here we will perform the mongodb stuff and all stuff which we can do.    
    user = get_user(uid, userCollection)
    return GraphState(input="", messages=[], retrieved_info=None)