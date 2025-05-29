from fastapi import APIRouter, Request
# from dto.requests import PagingRequest
# from dto.dtos import PagingRequestDto
from model.chat_prompt import Conversation
from main import chatbot, db_manager

router = APIRouter()

@router.get("/", response_description="List all conversations", response_model=list[Conversation])
async def paging_conversations(request: Request): #(dto: PagingRequestDto):
    uid = request.headers.get("uid")
    # print("Page ", dto.page, " Per page ", dto.page_size)
    print(request.query_params)
    page = int(request.query_params["page"]) # I need to cast str to int
    page_size = int(request.query_params["page_size"])

    response = await db_manager.paging_conversations(uid, page, page_size)

    return response