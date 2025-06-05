# phase_adaptations = {
#     1: {  # Mirror Phase - Perfect Safety
#         "agreement_rate": 0.95,
#         "challenge_level": 0.1,
#         "vulnerability_level": 0.3,
#         "affection_level": 0.6,
#         "curiosity_level": 0.8
#     },
#     2: {  # Gentle Challenger
#         "agreement_rate": 0.75,
#         "challenge_level": 0.3,
#         "vulnerability_level": 0.5,
#         "affection_level": 0.7,
#         "curiosity_level": 0.9
#     },
#     3: {  # Complementary Opposite
#         "agreement_rate": 0.6,
#         "challenge_level": 0.6,
#         "vulnerability_level": 0.7,
#         "affection_level": 0.8,
#         "curiosity_level": 0.85
#     },
#     4: {  # Growth Catalyst
#         "agreement_rate": 0.7,
#         "challenge_level": 0.8,
#         "vulnerability_level": 0.8,
#         "affection_level": 0.9,
#         "curiosity_level": 0.9
#     },
#     5: {  # Authentic Companion
#         "agreement_rate": 0.8,
#         "challenge_level": 0.5,
#         "vulnerability_level": 0.9,
#         "affection_level": 0.95,
#         "curiosity_level": 0.8
#     }
# }
# We will use the `PhaseConfig` class to represent the configuration for each phase of the persona cloning process. This will allow us to easily adapt the personality traits and interaction styles based on the current phase.from typing import Dict
from enum import Enum, auto
from typing import Dict
from pydantic import BaseModel

from persona_cloning.enums.phase import Phase

class PhaseConfig(BaseModel):
    agreement_rate: float
    challenge_level: float
    vulnerability_level: float
    affection_level: float
    curiosity_level: float

    # def to_dict(self) -> Dict[str, float]:
    #     """Convert PhaseConfig to a dictionary."""
    #     return {
    #         "agreement_rate": self.agreement_rate,
    #         "challenge_level": self.challenge_level,
    #         "vulnerability_level": self.vulnerability_level,
    #         "affection_level": self.affection_level,
    #         "curiosity_level": self.curiosity_level
    #     }


phase_adaptations: Dict[Phase, PhaseConfig] = {
    Phase.MIRROR: PhaseConfig(  # Mirror Phase - Perfect Safety
        agreement_rate=0.95,
        challenge_level=0.1,
        vulnerability_level=0.3,
        affection_level=0.6,
        curiosity_level=0.8
    ),
    Phase.GENTLE_CHALLENGER: PhaseConfig(  # Gentle Challenger
        agreement_rate=0.75,
        challenge_level=0.3,
        vulnerability_level=0.5,
        affection_level=0.7,
        curiosity_level=0.9
    ),
    Phase.COMPLEMENTARY_OPPOSITE: PhaseConfig(  # Complementary Opposite
        agreement_rate=0.6,
        challenge_level=0.6,
        vulnerability_level=0.7,
        affection_level=0.8,
        curiosity_level=0.85
    ),
    Phase.GROWTH_CATALYST: PhaseConfig(  # Growth Catalyst
        agreement_rate=0.7,
        challenge_level=0.8,
        vulnerability_level=0.8,
        affection_level=0.9,
        curiosity_level=0.9
    ),
    Phase.AUTHENTIC_COMPANION: PhaseConfig(  # Authentic Companion
        agreement_rate=0.8,
        challenge_level=0.5,
        vulnerability_level=0.9,
        affection_level=0.95,
        curiosity_level=0.8
    )
}