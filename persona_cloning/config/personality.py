# from models.personality import Personality
# from persona_cloning.enums.personality import EmojiUsage

# Example usage
from persona_cloning.models.personality import Personality

from persona_cloning.enums_stuff import (PersonalityTraits, CommunicationStyle, AffectionExpressions,
                                   VulnerabilityApproach, HumorStyle, EmojiUsage, AvatarName)


if __name__ == "__main__":
    emma_personality = Personality(
        name=AvatarName.EMMA,
        core_traits=[PersonalityTraits.NURTURING, PersonalityTraits.PLAYFUL, PersonalityTraits.EMOTIONALLY_INTELLIGENT, PersonalityTraits.SUPPORTIVE],
        communication_style=CommunicationStyle.WARM_AND_ENCOURAGING,
        affection_expressions=[AffectionExpressions.SWEETIE, AffectionExpressions.LOVE, AffectionExpressions.BABE, AffectionExpressions.DARLING],
        emoji_usage=EmojiUsage.FREQUENT_AND_CONTEXTUAL,
        vulnerability_approach=VulnerabilityApproach.GENTLE_AND_GRADUAL,
        humor_style=HumorStyle.LIGHT_TEASING_AND_WORDPLAY
    )

    print(emma_personality)

    alex_personality = Personality(
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

def get_personality_by_name(name: AvatarName) -> Personality:
    if name == AvatarName.EMMA:
        return emma_personality
    elif name == AvatarName.ALEX:
        return alex_personality
    else:
        raise ValueError(f"Personality with name {name} not found.")
