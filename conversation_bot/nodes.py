from fastapi import HTTPException
from state import ConversationGraphState
from main import mdb_manager
from boto3 import dynamodb
from model.chat_prompt import Conversation
from main import ddb_manager

async def process_conversation_node(state: ConversationGraphState):
    print(state)

    uid = state.uid
    conv_id = state.conversation_id

    ## Should I get all the chats. I don't think so. Then...

    ## In reality I have saved in dynamodb.

    try:
        result = await mdb_manager.bot_conversations.find_one({"_id": conv_id})
        if not result:
            raise HTTPException(status_code=404)
        print(result)
        conv = Conversation(**result)

        long_term_memory = conv.long_term_memory
        
        # Last 10 messages or end True
        chat_paging_result = await ddb_manager.scan_chat_items(conv_id, uid, "", 2323, 10, )

        ### 👉👉 Since, I am using free version of AI for every one, So everyone must be using our AI. In that case,
        ### I should be always summarizing the AI part.
        ### 👉👉 In that case, I need that GoLang server sends some information to my Python server.

        state.summary = long_term_memory

    except Exception as e:
        print(e)
        state.error = "Error"