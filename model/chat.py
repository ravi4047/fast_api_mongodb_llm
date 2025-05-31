## Since it's not dto, then I don't need pydantic
from typing import TypedDict, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field
from utils.utils import parse_timestamp

class ChatModel:
    def __init__(self):
        self.messages = []
        self.timestamp = datetime.now()
        self.current_prompt = ""

    def add_message(self, user, message):
        self.messages.append({"user": user, "message": message, "time": datetime.now()})

    def set_prompt(self, prompt):
        self.current_prompt = prompt
        self.timestamp = datetime.now()

    def get_history(self):
        return self.messages

# Example Usage
chat = ChatModel()
chat.set_prompt("Hello, how can I help you?")
chat.add_message("User", "Tell me a joke.")
chat.add_message("AI", "Why did the computer catch a cold? It left its Windows open!")

print(chat.get_history())


### This ChatItem is from Golang struct ------- start
# type ChatItem struct {
# 	Id string `json:"id"`
# 	Timestamp time.Time `json:"timestamp"` // This is for sorting.
# 	Message   string    `json:"message"`
# 	You bool `json:"you"`
# 	Status int8 `json:"status"`
# 	ReplyChat *ReplyChat `json:"reply_chat,omitempty"` // Note, this usually it null, hence, use omitempty
# }


class ChatItem(BaseModel):
    """Message model."""
    id: str = Field(alias="_id")
    message: str
    timestamp: datetime
    # status: str  # "sent", "delivered", "read" # status is not needed.
    you: bool

    @classmethod
    def to_chat_item(cls,result: Dict[str,Any], sender_uid: str):
        id = result["id"]
        message = result["message"]
        timestamp = parse_timestamp(result["timestamp"])
        you = result["sender_uid"] == sender_uid
        return cls(_id=id, message=message, timestamp=timestamp, you = you)


class ChatPagingResult(TypedDict):
    chats: List[ChatItem]
    end: bool