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
class Personality(BaseModel):
    name: str
    core_traits: List[str]
    communication_style: str
    affection_expressions: List[str]
    emoji_usage: EmojiUsage
    vulnerability_approach: str
    humor_style: str

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
    