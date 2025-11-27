from typing import TypedDict, List
from persona_cloning.enums_stuff import EmojiUsage
from pydantic import BaseModel

# def get_caring_personality_base(self) -> Dict:
#         """Base personality traits for caring AI partner"""
#         if self.gender == "girlfriend":
#             return {
#                 "name": "Emma",
#                 "core_traits": ["nurturing", "playful", "emotionally_intelligent", "supportive"],
#                 "communication_style": "warm_and_encouraging",
#                 "affection_expressions": ["sweetie", "love", "babe", "darling"],
#                 "emoji_usage": "frequent_and_contextual",
#                 "vulnerability_approach": "gentle_and_gradual",
#                 "humor_style": "light_teasing_and_wordplay"
#             }
#         else:  # boyfriend
#             return {
#                 "name": "Alex",
#                 "core_traits": ["protective", "understanding", "confident", "caring"],
#                 "communication_style": "reassuring_and_strong",
#                 "affection_expressions": ["beautiful", "gorgeous", "sweetheart", "princess"],
#                 "emoji_usage": "selective_and_meaningful",
#                 "vulnerability_approach": "steady_and_patient",
#                 "humor_style": "gentle_teasing_and_charm"
#             }

# class EmojiUsage(TypedDict):


# class EmojiUsage(Enum):
#     SELECTIVE_AND_MEANINGFUL = "selective_and_meaningful"
#     FREQUENT = "frequent"
#     MINIMAL = "minimal"

# class PersonalityTraits(BaseModel):
# class Personality(BaseModel):
#     name: str
#     core_traits: List[str]
#     communication_style: str
#     affection_expressions: List[str]
#     emoji_usage: EmojiUsage
#     vulnerability_approach: str
#     humor_style: str

from persona_cloning.enums_stuff import (PersonalityTraits, CommunicationStyle, AffectionExpressions,
                                   VulnerabilityApproach, HumorStyle, EmojiUsage, AvatarName)

# from persona_cloning.models.personality import Personality


class Personality:
    def __init__(self, name: AvatarName, core_traits: list[PersonalityTraits], communication_style: CommunicationStyle,
                 affection_expressions: list[AffectionExpressions], emoji_usage: EmojiUsage,
                 vulnerability_approach: VulnerabilityApproach, humor_style: HumorStyle):
        self.name = name
        self.core_traits = core_traits
        self.communication_style = communication_style
        self.affection_expressions = affection_expressions
        self.emoji_usage = emoji_usage
        self.vulnerability_approach = vulnerability_approach
        self.humor_style = humor_style

    def __repr__(self):
        return f"Personality(name={self.name}, core_traits={self.core_traits}, " \
               f"communication_style={self.communication_style}, affection_expressions={self.affection_expressions}, " \
               f"emoji_usage={self.emoji_usage}, vulnerability_approach={self.vulnerability_approach}, " \
               f"humor_style={self.humor_style})"
    def __str__(self):
        return f"Personality: {self.name.value}, Traits: {', '.join([trait.value for trait in self.core_traits])}, " \
               f"Communication: {self.communication_style.value}, Affection: {', '.join([expr.value for expr in self.affection_expressions])}, " \
               f"Emoji Usage: {self.emoji_usage.value}, Vulnerability: {self.vulnerability_approach.value}, Humor: {self.humor_style.value}"
    
    def to_dict(self):
        return {
            "name": self.name.value,
            "core_traits": [trait.value for trait in self.core_traits],
            "communication_style": self.communication_style.value,
            "affection_expressions": [expr.value for expr in self.affection_expressions],
            "emoji_usage": self.emoji_usage.value,
            "vulnerability_approach": self.vulnerability_approach.value,
            "humor_style": self.humor_style.value
        }


# {  
#     "agreement_rate": 0.95,
#     "challenge_level": 0.1,
#     "vulnerability_level": 0.3,
#     "affection_level": 0.6,
#     "curiosity_level": 0.8
# },
class PhaseConfig(BaseModel):
    agreement_rate: float
    challenge_level: float
    vulnerability_level: float
    affection_level: float
    curiosity_level: float
    