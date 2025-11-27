# This is a one server only for now, so we can use a simple in-memory store for the user chats
# and emotions. -- Temporary solution, replace with a aws elasticache or similar in production.
# https://claude.ai/chat/c5d85244-f76c-4e20-ab60-eab33b9d9ca5
# https://aws.amazon.com/elasticache/pricing/
# https://chatgpt.com/c/68417a30-cf6c-800d-a693-909681d6e6ac

# Let's create a proper in-memory chat store, later we can replace it with a cache solution.
# Database would actually be slow and expensive for this use case.
from typing import Dict, List
from datetime import datetime

from dto.persona import AiCompanionDto
# from persona_cloning.models.ai_companion import AiCompanion
from model.user_profile import UserProfile
from persona_cloning.models.emotion import EmotionalState

from config.config import MAX_RECENT_CHAT_MESSAGES

class ChatEntry:
    def __init__(self,  message: str, timestamp: datetime, is_ai: bool):
        """Initialize a chat entry with user ID, message, and timestamp."""
        # self.user_id = user_id
        self.is_ai = is_ai
        self.message = message
        self.timestamp = timestamp

class ConversationStore:
    def __init__(self, user_profile: UserProfile, conversation_id: str, connection_id: str, ai_companion: AiCompanionDto):
        """Initialize the chat store for a specific user."""
        # self.user_id = user_id
        self.user_profile = user_profile 
        self.conversation_id = conversation_id

        ## Maybe used for WebSocket connections or similar
        # This could be useful for tracking connections in a real-time chat application
        # Note, there can be multiple connections for the same user
        self.connection_id = connection_id
        self.ai_companion = ai_companion

        self._max_token_limit = 10000  # Set a maximum token limit for the user
        self._current_token_count = 0  # Initialize token count for the user

        # Dictionary to hold user chats, mapping user_id to a list of ChatEntry objects
        # self._chats: Dict[str, List[ChatEntry]] = {}
        self._recent_chats: List[ChatEntry] = []  # Store only the most recent chats for the user

        # I need conversation history summary
        # https://chatgpt.com/c/6842dbb9-19b0-800d-80a1-0655f186a8cf
        # (AI) This could be a summary of the conversation history, useful for context in responses
        self._conversation_summary = ""

        # Emotional state
        self._emotional_state = EmotionalState(
            dominant_emotions=[],
            emotional_complexity=0.0,
            emotional_stability=0.0,
            transition_type="stable",
            arousal_level=0.0,
            valence=0.0,
            timestamp=datetime.now()
        )

        self.ai_companion = AiCompanionDto(
            name=ai_companion.name,
            age=ai_companion.age,
            personality=ai_companion.personality
        )

    def add_recent_chat(self, message: str, timestamp: datetime, is_ai: bool):
        """Add a recent chat entry for the user, keeping only the most recent N chats."""
        entry = ChatEntry( message, timestamp, is_ai)
        self._recent_chats.append(entry)
        max_chats = MAX_RECENT_CHAT_MESSAGES  # Limit to the most recent N chats
        if len(self._recent_chats) > max_chats:
            # Remove oldest chats to keep only the most recent max_chats
            self._recent_chats = self._recent_chats[-max_chats:]

    def get_recent_chats(self) -> List[ChatEntry]:
        """Get the most recent chat entries for the user."""
        return self._recent_chats

    # keeping only the most recent N chats.
    # def add_chat(self, message: str, timestamp: datetime):
    #     """Add a chat entry for the user, keeping only the most recent N chats."""
    #     entry = ChatEntry(self.user_id, message, timestamp)
    #     chats = self._chats.setdefault(self.user_id, [])
    #     chats.append(entry)
    #     max_chats = 20  # Limit to the most recent 20 chats
    #     if len(chats) > max_chats:
    #         # Remove oldest chats to keep only the most recent max_chats
    #         self._chats[self.user_id] = chats[-max_chats:]

    # # def get_chats_by_user(self, user_id: str) -> List[ChatEntry]:
    # #     """Get all chat entries for a specific user."""
    # #     return self._chats.get(user_id, [])


    # def get_chats(self) -> List[ChatEntry]:
    #     return self._chats.get(self.user_id, [])

    # def clear_chats(self):
    #     if self.user_id in self._chats:
    #         del self._chats[self.user_id]

    # Setters for emotional state
    def set_emotional_state(self, emotional_state: EmotionalState):
        """Set the emotional state for the user."""
        self._emotional_state = emotional_state

    def get_emotional_state(self) -> EmotionalState:
        """Get the emotional state for the user."""
        return self._emotional_state
    
    # Increment the token count
    def increment_token_count(self, tokens: int):
        """Increment the current token count by a specified number of tokens."""
        self._current_token_count += tokens
        if self._current_token_count > self._max_token_limit:
            raise ValueError("Token limit exceeded")
        
    def get_token_count(self) -> int:
        """Get the current token count."""
        return self._current_token_count
    
    # Get the leftover token count
    def get_leftover_token_count(self) -> int:
        """Get the number of tokens left before reaching the maximum limit."""
        return self._max_token_limit - self._current_token_count
    

class ConversationStoreManager:
    def __init__(self):
        self.stores: Dict[str, ConversationStore] = {}

    # def get_store(self, user_id: str, conversation_id: str, connection_id: str) -> ChatStore:
    #     # Conversation id is enough as only conversation per session.
    #     key = f"{user_id}_{conversation_id}"
    #     if key not in self.stores:
    #         self.stores[key] = ChatStore(user_id, conversation_id, connection_id)
    #     return self.stores[key]

    # def clear_store(self, user_id: str, conversation_id: str):
    #     key = f"{user_id}_{conversation_id}"
    #     if key in self.stores:
    #         del self.stores[key]

    def get_store(self, connection_id: str) -> ConversationStore:
        # Use conversation_id as the unique key per connection/session.
        # [update] conversation id is not unique as there can be multiple connections for the same user.
        # key = conversation_id
        key = connection_id
        if key not in self.stores:
            # self.stores[key] = ConversationStore(user_id, conversation_id, connection_id, ai_companion)
            # Error will be raise if key is not found
            raise ValueError(f"Conversation store for {key} not found. Please set the conversation store first.")
        return self.stores[key]

    # def clear_store(self, conversation_id: str):
    #     key = conversation_id
    #     if key in self.stores:
    #         del self.stores[key]
    def clear_store(self, connection_id: str):
        key = connection_id
        if key in self.stores:
            del self.stores[key]

    def set_conversation_store(self, user_profile: UserProfile, conversation_id: str, connection_id: str, ai_companion: AiCompanionDto):
        """Set or update the conversation store for a user."""
        self.stores[connection_id] = ConversationStore(
            user_profile=user_profile,
            conversation_id=conversation_id,
            connection_id=connection_id,
            ai_companion=ai_companion
        )

# Create a global instance of ChatStoreManager
conv_store_manager = ConversationStoreManager()