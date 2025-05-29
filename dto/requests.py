from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Literal

# class PagingRequest(BaseModel):
#     # user_id: str ## The uid will be in the headers I guess.
#     page: int
#     page_size: int

# 👉 In future you will split the file if many are there.

# 👉 Still dtos are better


class PostBio(BaseModel):
    bio: str

# https://claude.ai/chat/537f692e-323c-43ad-9c43-fc5e17f416f8
class BioGenerationRequest(BaseModel):
    # user_id: str
    user_description: str = Field(max_length=500)
    tone: Optional[str] =  Field(
        default="friendly",
        #   regex="^(casual|friendly|witty|professional|romantic)$",
            # union_mode=Literal["ca"]
            pattern="^(casual|friendly|witty|professional|romantic)$",
            )
    bio_length: Optional[str] = Field(default="medium",
                                    #    regex="^(short|medium|long)$"
                                       pattern="^(short|medium|long)$"
                                       )