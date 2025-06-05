# from models.personality import Personality
# from persona_cloning.enums.personality import EmojiUsage
from persona_cloning.enums_stuff import (PersonalityTraits, CommunicationStyle, AffectionExpressions,
                                   VulnerabilityApproach, HumorStyle, EmojiUsage, AvatarName)

from persona_cloning.models.personality import Personality


class PersonalityConfig:
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
        return f"PersonalityConfig(name={self.name}, core_traits={self.core_traits}, " \
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
# Example usage
if __name__ == "__main__":
    emma_personality = PersonalityConfig(
        name=AvatarName.EMMA,
        core_traits=[PersonalityTraits.NURTURING, PersonalityTraits.PLAYFUL, PersonalityTraits.EMOTIONALLY_INTELLIGENT, PersonalityTraits.SUPPORTIVE],
        communication_style=CommunicationStyle.WARM_AND_ENCOURAGING,
        affection_expressions=[AffectionExpressions.SWEETIE, AffectionExpressions.LOVE, AffectionExpressions.BABE, AffectionExpressions.DARLING],
        emoji_usage=EmojiUsage.FREQUENT_AND_CONTEXTUAL,
        vulnerability_approach=VulnerabilityApproach.GENTLE_AND_GRADUAL,
        humor_style=HumorStyle.LIGHT_TEASING_AND_WORDPLAY
    )

    print(emma_personality)

    alex_personality = PersonalityConfig(
        name=AvatarName.ALEX,
        core_traits=[PersonalityTraits.PROTECTIVE, PersonalityTraits.UNDERSTANDING, PersonalityTraits.CONFIDENT, PersonalityTraits.CARING],
        communication_style=CommunicationStyle.REASSURING_AND_STRONG,
        affection_expressions=[AffectionExpressions.BEAUTIFUL, AffectionExpressions.GORGEOUS, AffectionExpressions.SWEETHEART, AffectionExpressions.PRINCESS],
        emoji_usage=EmojiUsage.SELECTIVE_AND_MEANINGFUL,
        vulnerability_approach=VulnerabilityApproach.STEADY_AND_PATIENT,
        humor_style=HumorStyle.GENTLE_TEASING_AND_CHARM
    )
    print(alex_personality)
    # Add more personalities as needed
