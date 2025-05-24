from pydantic import BaseModel

class ChatRequestDto(BaseModel):
    uid: str
    prompt: str
    

# print(Model(items=(1, 2, 3)))