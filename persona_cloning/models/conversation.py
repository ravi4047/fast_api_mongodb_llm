# {
#     "timestamp": datetime.now(),
#     "dimension_explored": dimension,
#     "specific_area": specific_area,
#     "phase": self.current_phase,
#     "session_number": self.session_count
# }
# The above is a dictionary that represents the conversation history.

# Let's create a Conversation class to represent the conversation history.

from pydantic import BaseModel

class Conversation(BaseModel):
    """Conversation model"""
    id: str
    title: str
    uid: str
    timestamp: str  # Using string for simplicity, can be datetime if needed
    long_term_memory: str  # This is for conversation.

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def create(cls, title: str, uid: str, timestamp: str):
        """Create and return a new Conversation instance"""
        return cls(id="", title=title, uid=uid, timestamp=timestamp, long_term_memory="")