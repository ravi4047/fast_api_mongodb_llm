from persona_cloning.models.personality import Personality


class AiCompanion:
    def __init__(self, name: str, age: int, personality: Personality):
        self.name = name
        self.age = age
        # self.description = description
        self.personality = personality

    # def greet(self) -> str:
    #     return f"Hello, I am {self.name}. {self.description}"

    # def respond(self, message: str) -> str:
    #     return f"{self.name} responds: {message}"