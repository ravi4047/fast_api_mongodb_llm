# This is a one server only for now, so we can use a simple in-memory store for the user chats
# and emotions. -- Temporary solution, replace with a aws elasticache or similar in production.
# https://claude.ai/chat/c5d85244-f76c-4e20-ab60-eab33b9d9ca5
# https://aws.amazon.com/elasticache/pricing/
# https://chatgpt.com/c/68417a30-cf6c-800d-a693-909681d6e6ac

# Let's create a proper in-memory chat store, later we can replace it with a cache solution.
# Database would actually be slow and expensive for this use case.
from typing import Dict, List

class ChatEntry:
    def __init__(self, user_id: str, message: str):
        self.user_id = user_id
        self.message = message

class ChatStore:
    def __init__(self, user_id: str, conversation_id: str, connection_id: str):
        """Initialize the chat store for a specific user."""
        self.user_id = user_id
        self.conversation_id = conversation_id

        ## Maybe used for WebSocket connections or similar
        # This could be useful for tracking connections in a real-time chat application
        # Note, there can be multiple connections for the same user
        self.connection_id = connection_id

        self.max_token_limit = 10000  # Set a maximum token limit for the user
        self.current_token_count = 0  # Initialize token count for the user

        # Dictionary to hold user chats, mapping user_id to a list of ChatEntry objects
        self.chats: Dict[str, List[ChatEntry]] = {}

    def add_chat(self, message: str):
        entry = ChatEntry(self.user_id, message)
        self.chats.setdefault(self.user_id, []).append(entry)

    def get_chats(self) -> List[ChatEntry]:
        return self.chats.get(self.user_id, [])

    def clear_chats(self):
        if self.user_id in self.chats:
            del self.chats[self.user_id]


class ChatStoreManager:
    def __init__(self):
        self.stores: Dict[str, ChatStore] = {}

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

    def get_store(self, user_id: str, conversation_id: str, connection_id: str) -> ChatStore:
        # Use conversation_id as the unique key per connection/session.
        key = conversation_id
        if key not in self.stores:
            self.stores[key] = ChatStore(user_id, conversation_id, connection_id)
        return self.stores[key]

    def clear_store(self, conversation_id: str):
        key = conversation_id
        if key in self.stores:
            del self.stores[key]


# Create a global instance of ChatStoreManager
chat_store_manager = ChatStoreManager()