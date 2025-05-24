from fastapi import APIRouter, Request, Response

from typing import Optional, List
from model.chat import ChatModel

from pymongo.collection import Collection

from dto.chat_request_dto import ChatRequestDto

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
def chat_endpoint(data: ChatRequestDto, request: Request):
    """
    API endpoint to interact with the chatbot using langgraph and search tools.
    It dynamically selects the model specified in the request.
    """
    uid = request.headers.get("uid")
    
    chatData = data.model_json_schema()
    print("chat data", chatData)

    return