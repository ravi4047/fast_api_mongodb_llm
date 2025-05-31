from langgraph.graph import StateGraph, END

from state import ConversationGraphState

from langgraph.checkpoint.mongodb import AsyncMongoDBSaver

from nodes import process_conversation_node

## First I will focus Conversation, then I will shift to MatchMaking

## 👉👉 I need graph to save the memory, otherwise I would have worked without LangGraph even.

PROCESS_CONVERSATION_NODE = "PROCESS_CONVERSATION_NODE"

async def create_graph():
    """Create the LangGraph workflow"""
    workflow = StateGraph(ConversationGraphState)
    workflow.add_node(PROCESS_CONVERSATION_NODE, process_conversation_node)

    workflow.set_entry_point(PROCESS_CONVERSATION_NODE)
    workflow.set_finish_point(PROCESS_CONVERSATION_NODE)

    # This code is from the AsyncMongoDBSaver documentation only.
    async with AsyncMongoDBSaver.from_conn_string("", db_name="my_db", checkpoint_collection_name="", writes_collection_name="") as memory:
        workflow.compile(checkpointer=memory)