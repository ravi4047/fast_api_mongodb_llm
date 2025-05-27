from pydantic import BaseModel
from typing import Optional, Dict, Any

# class ChatRequestDto(BaseModel):
#     uid: str
#     prompt: str

# # print(Model(items=(1, 2, 3)))

class ChatRequest(BaseModel):
    user_id: str
    message: str
    context: Optional[Dict[str, Any]] = None