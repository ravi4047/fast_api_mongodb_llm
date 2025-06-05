## auto() is used to automatically assign unique values to each enum member
from enum import Enum, auto

class Phase(Enum):
    # phase_multiplier = {1: 1.0, 2: 1.2, 3: 1.5, 4: 1.8, 5: 2.0}
    MIRROR = ("NURTURING", 1.0)
    GENTLE_CHALLENGER = ("PLAYFUL", 1.2)
    COMPLEMENTARY_OPPOSITE = ("ENERGETIC", 1.5)
    GROWTH_CATALYST = ("WISE", 1.8)
    AUTHENTIC_COMPANION = ("ROMANTIC", 2.0)

    def __init__(self, mood: str, phase_multiplier: float = 1.0):
        self.mood = mood
        self.phase_multiplier = phase_multiplier

    @property
    def mood_name(self) -> str:
        return self.mood[0]

    @property
    def mood_type(self) -> type:
        return type(self.mood)
    
    @property
    def phase_multiplier_value(self) -> float:
        return self.phase_multiplier