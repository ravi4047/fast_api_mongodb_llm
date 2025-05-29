from typing import TypedDict, List
from pydantic import BaseModel

## When lots of classes are there, I will switch to folder mode.

# Using TypedDict, 
class BioMakerResponse(TypedDict):
    type: str # response or error type
    content: str

# https://claude.ai/chat/537f692e-323c-43ad-9c43-fc5e17f416f8
class BioResponse(BaseModel):
    generated_bio: str
    safety_flags: List[str]
    suggestions: List[str]