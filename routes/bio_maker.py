from fastapi import APIRouter, Request, Depends

from typing import List

from token_and_rate_limiting_system.token_limiting import get_user_id

router = APIRouter()

@router.post("/bio", response_description="List all books",) # response_model=List[],)
async def post_bio_maker(user_id = Depends(get_user_id)):
    """
    API endpoint to interact with the chatbot using langgraph and search tools.
    It dynamically selects the model specified in the request.
    """
    
    print("user id", user_id)    

    return {
        
    }