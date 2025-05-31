from fastapi import APIRouter, Request, Response

from typing import Optional, List
from model.chat import ChatModel
from model.chat_prompt import ChatPrompt

from pymongo.collection import Collection

from dto.chat_request_dto import ChatRequest

from main import mdb_manager

router = APIRouter()

@router.get("/", response_description="List all books", response_model=List[ChatModel])
def list_chats(request: Request): 
    # myCollection = request.app.database["my_collection"]
    # books = list(request.app.database["books"].find(limit=100))

    # # book2 = Collection(request.app.database["my_collection"])
    # # book2
    # books2 = bookCollection(request.app.database).find(limit=100)

    chatCollection: Collection = request.app.database["chat"]

    # chatCollection: Collection = request.app.database["chat"]

    # chatCollection.find(limit=100)

    return 

@router.post("/chat", response_description="Just do success true")
def chat_endpoint(data: ChatRequest, request: Request):
    """
    API endpoint to interact with the chatbot using langgraph and search tools.
    It dynamically selects the model specified in the request.
    """
    uid = request.headers.get("uid")
    
    chatData = data.model_json_schema()
    print("chat data", chatData)

    return

@router.get("/", response_description="List all books", response_model=List[ChatPrompt])
async def paging_chats(request: Request):
    uid = request.headers.get("uid")
    print(request.query_params)
    page = int(request.query_params["page"]) # I need to cast str to int
    page_size = int(request.query_params["page_size"])

    response = await mdb_manager.paging_chat_prompts(uid, page, page_size)

    return response