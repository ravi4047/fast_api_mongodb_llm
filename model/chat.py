## Since it's not dto, then I don't need pydantic
from typing import TypedDict
from datetime import datetime

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