# Big 5 traits
from pydantic import BaseModel, Field
from enum import Enum, auto
from typing import Dict, List

class Big5Trait(str, Enum):
    OPENNESS = ("openness")  # Openness to Experience
    CONSCIENTIOUSNESS = ("conscientiousness")  # Conscientiousness
    EXTRAVERSION = ("extraversion")  # Extraversion
    AGREEABLENESS = ("agreeableness")  # Agreeableness
    NEUROTICISM = ("neuroticism")  # Neuroticism

class Big5TraitsModel(BaseModel):
    openness: float = Field(0.5, description="Openness to Experience")
    conscientiousness: float = Field(0.5, description="Conscientiousness")
    extraversion: float = Field(0.5, description="Extraversion")
    agreeableness: float = Field(0.5, description="Agreeableness")
    neuroticism: float = Field(0.5, description="Neuroticism")

    def to_dict(self) -> Dict[str, float]:
        """Convert Big5TraitsModel to a dictionary."""
        return self.model_dump()
    
    # Add methods to modify traits
    def add_openness(self, value: float):
        self.openness += value

    def add_conscientiousness(self, value: float):
        self.conscientiousness += value

    def add_extraversion(self, value: float):
        self.extraversion += value

    def add_agreeableness(self, value: float):
        self.agreeableness += value

    def add_neuroticism(self, value: float):
        self.neuroticism += value

# class Big5Traits(): #(Enum):
#     # OPENNESS = 0.5  # Openness to Experience
#     # CONSCIENTIOUSNESS = 0.5  # Conscientiousness
#     # EXTRAVERSION = 0.5  # Extraversion
#     # AGREEABLENESS = 0.5  # Agreeableness
#     # NEUROTICISM = 0.5  # Neuroticism

#     openness: float = 0.5          # Openness to Experience
#     conscientiousness: float = 0.5 # Conscientiousness
#     extraversion: float = 0.5      # Extraversion
#     agreeableness: float = 0.5     # Agreeableness
#     neuroticism: float = 0.5        # Neuroticism

#     def add_openness(self, value: float):
#         self.openness += value

#     def add_conscientiousness(self, value: float):
#         self.conscientiousness += value

#     def add_extraversion(self, value: float):
#         self.extraversion += value

#     def add_agreeableness(self, value: float):
#         self.agreeableness += value

#     def add_neuroticism(self, value: float):
#         self.neuroticism += value

#     def to_dict(self) -> Dict[str, float]:
#         """Convert Big5Traits to a dictionary."""
#         return {
#             "openness": self.openness,
#             "conscientiousness": self.conscientiousness,
#             "extraversion": self.extraversion,
#             "agreeableness": self.agreeableness,
#             "neuroticism": self.neuroticism
#         }