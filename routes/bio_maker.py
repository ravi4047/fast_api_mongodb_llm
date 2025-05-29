from fastapi import APIRouter, Request, Depends, HTTPException

from typing import List

# from chatbot.bio_bot import BioBot # Not from here dude, but singleton one i.e. main.py one
from bio_maker.bio_enhancer import BioEnhancer
from bio_maker.prompt import BioPromptGenerator
from bio_maker.utils import ContentFilter
from main import biobot, db_manager
from dto.requests import BioGenerationRequest, PostBio
from responses import BioResponse

import logging

logger = logging.getLogger(__name__)

# from token_and_rate_limiting_system.token_limiting import get_user_id

router = APIRouter()

# @router.post("/bio", response_description="List all books",) # response_model=List[],)
# async def post_bio_maker(user_id = Depends(get_user_id)):
#     """
#     API endpoint to interact with the chatbot using langgraph and search tools.
#     It dynamically selects the model specified in the request.
#     """
    
#     print("user id", user_id)    

#     return {
        
#     }

### This was my code. It was nice ------------------------ start
# @router.post("", response_description="Post bio", response_model=str)
# async def post_bio_maker(request: Request, postBio: PostBio):
#     """
#     API endpoint to interact with the bio maker bot.
#     """
#     uid = request.headers.get("uid")
#     if uid is None:
#         raise HTTPException(status_code=400)

#     resp = await biobot.run_bio_maker(uid=uid, input=postBio.bio)

#     return resp
### This was my code. It was nice ------------------------ stop

# https://claude.ai/chat/537f692e-323c-43ad-9c43-fc5e17f416f8
## This one has really shut my mouth up. I am speechless
# Main API endpoints
@router.post("/generate-bio", response_model=BioResponse)
async def generate_bio(req: Request, request: BioGenerationRequest):
    """Generate a dating app bio based on user description and profile"""
    try:
        uid = req.headers.get("uid")
        if not uid:
            raise HTTPException(status_code=400)

        # Get user profile
        user_profile = await db_manager.get_user_profile(uid)
        
        # Check content safety
        safety_flags = ContentFilter.check_content_safety(request.user_description)
        
        # Generate prompt
        prompt = BioPromptGenerator.generate_prompt(
            user_profile=user_profile,
            user_description=request.user_description,
            tone=request.tone or "friendly",
            bio_length=request.bio_length or "medium"
        )
        
        # Generate bio with LLM
        # raw_bio = await generate_bio_with_llm(prompt)
        raw_bio = await biobot.run_llm(prompt)
        
        # Enhance and clean up bio
        enhanced_bio = BioEnhancer.enhance_bio(raw_bio, user_profile)
        
        # Final safety check on generated bio
        final_safety_flags = ContentFilter.check_content_safety(enhanced_bio)
        all_safety_flags = list(set(safety_flags + final_safety_flags))
        
        # Generate suggestions
        suggestions = BioEnhancer.generate_suggestions(user_profile, all_safety_flags)
        
        # Log generation for monitoring
        logger.info(f"Bio generated for user {uid}, flags: {all_safety_flags}")
        
        return BioResponse(
            generated_bio=enhanced_bio,
            safety_flags=all_safety_flags,
            suggestions=suggestions
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in bio generation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")