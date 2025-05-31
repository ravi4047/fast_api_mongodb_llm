from state import BioGraphState
from main import mdb_manager
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Input and output both same
async def process_bio_input_node(state: BioGraphState)-> BioGraphState:
    print("state", state.values())

    uid = state["uid"]
    input = state["input"]

    profile = await mdb_manager.get_user_profile(uid)

    ## Setting the profile in this node.
    state["profile"] = profile

    return state

async def run_graph_node(state: BioGraphState)->BioGraphState:
    print("state", state.values())

    # The whole code is made by me.

    chat_prompts = [
        SystemMessage(""),
        HumanMessage("")
    ]

    print(chat_prompts)

    return state