# from langchain.tools import tool
from langchain.agents import tool
from pymongo.collection import Collection
from agent.graph import GraphState
## The tools will respond with personal information about user.

# @tool

## Plan change -> In tools, we won't access the mongodb collection (Obviously).
# 👉👉 We just use the tool to know that this tool will run which will tell this get user birthday stuff to run.

# https://chatgpt.com/c/681f72e4-5ad0-800d-b706-dc2453ab111e


@tool
def get_user_birthday(playerName:str, uid: str, playerCollection: Collection, state: GraphState)->GraphState:
    """
    Get birthday of the person.
    """
    player = playerCollection.find_one({"_id": uid})

    if player:
        info = f"User info: {player}"
    else:
        info = "No matching user found."

    ## Why not type strictness
    # return {
    #     "messages": state["messages"],
    #     "input": state["input"],
    #     "retrieved_info": info,
    # }
    return GraphState(messages=state["messages"], input=state["input"], retrieved_info=info)

# @tool
# def get_user_bio(playerName:str, uid: str, playerCollection: Collection, state: GraphState)->GraphState:

# So https://chatgpt.com/c/681f72e4-5ad0-800d-b706-dc2453ab111e
# 👉👉 The tool is provided to just add the condition only. Oh wait, we have already defined stuff like these.
# No, But we can't end it like this.

### I finally understood the case.

@tool
def fetch_person_info(person_name: str, user_id: str) -> str:
    """Fetch information about the person user is interested in.
    Requires person_name from LLM and user_id from auth context."""
    # Use MongoDB etc.
    return f"Info about {person_name} for user {user_id}"