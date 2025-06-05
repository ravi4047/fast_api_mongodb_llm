# def initialize_persona_scores(self) -> dict[str, dict[str, float]]:
#         """Initialize the 8-dimension scoring system"""
#         return {
#             "emotional_dna": {
#                 "score": 0,
#                 "emotional_range_mapping": 0,
#                 "stress_response_pattern": 0,
#                 "vulnerability_comfort_zone": 0,
#                 "empathy_style": 0,
#                 "emotional_recovery_pattern": 0
#             },
#             "communication_blueprint": {
#                 "score": 0,
#                 "conflict_resolution_style": 0,
#                 "conversation_rhythm": 0,
#                 "humor_playfulness": 0,
#                 "serious_discussion_approach": 0,
#                 "love_language_expression": 0
#             },
#             "values_belief_system": {
#                 "score": 0,
#                 "life_priorities_hierarchy": 0,
#                 "ethical_decision_framework": 0,
#                 "relationship_philosophy": 0,
#                 "future_vision_clarity": 0
#             },
#             "personality_authenticity": {
#                 "score": 0,
#                 "big_five_traits": 0,
#                 "social_vs_private_self": 0,
#                 "decision_making_style": 0,
#                 "spontaneity_vs_planning": 0
#             },
#             "relationship_readiness": {
#                 "score": 0,
#                 "attachment_style_clarity": 0,
#                 "compromise_flexibility": 0,
#                 "intimacy_comfort_levels": 0,
#                 "partnership_expectations": 0
#             },
#             "life_compatibility_matrix": {
#                 "score": 0,
#                 "lifestyle_preferences": 0,
#                 "financial_philosophy": 0,
#                 "family_future_planning": 0,
#                 "career_ambition_balance": 0
#             },
#             "growth_challenge_threshold": {
#                 "score": 0,
#                 "learning_style_preferences": 0,
#                 "comfort_zone_expansion": 0,
#                 "feedback_reception": 0,
#                 "personal_development_drive": 0
#             },
#             "intuitive_connection": {
#                 "score": 0,
#                 "energy_vibe_patterns": 0,
#                 "unspoken_needs_detection": 0,
#                 "subtle_communication_cues": 0,
#                 "emotional_resonance_frequency": 0
#             }
#         }
# The above code represents eight distinct dimensions of the persona. Let's change the above code to models
from typing import List, Dict
from pydantic import BaseModel
from persona_cloning.enums_stuff import EmojiUsage

class PersonaScore(BaseModel):
    score: float

    def set_score(self, value: float):
        """Set the score for the persona dimension."""
        self.score = value


    def add_score(self, value: float):
        """Add a value to the current score."""
        self.score += value

    def set_attribute_score(self, attribute: str, value: float):
        """Set the score for a specific attribute."""
        if hasattr(self, attribute):
            setattr(self, attribute, value)
        else:
            raise ValueError(f"Attribute '{attribute}' does not exist in {self.__class__.__name__}.")

    def add_attribute_score(self, attribute: str, value: float):
        """Add the score for a specific attribute."""
        if hasattr(self, attribute):
            current_value = getattr(self, attribute, 0)
            setattr(self, attribute, current_value + value) 
        else:
            raise ValueError(f"Attribute '{attribute}' does not exist in {self.__class__.__name__}.")
        
    # Calculate the total score of all attributes except the main score
    def total_attributes_score(self) -> float:
        """Calculate the total score of all attributes."""
        total = 0
        for attr, value in self.model_dump().items():
            if attr != 'score':
                total += value
        return total
    
    def is_all_attributes_greater_than_0(self) -> bool:
        """Check if all attributes except the main score are greater than 0."""
        for attr, value in self.model_dump().items():
            if attr != 'score' and value <= 0:
                return False
        return True

class EmotionalDNA_PersonaScore(PersonaScore):
    initial_mood_assessment: float
    emotional_range_mapping: float
    stress_response_pattern: float
    vulnerability_comfort_zone: float
    empathy_style: float
    emotional_recovery_pattern: float



    # # Sum of all scores
    # def total_attributes_score(self) -> float:
    #     """Calculate the total score of all attributes."""
    #     return (
    #         self.initial_mood_assessment +
    #         self.emotional_range_mapping +
    #         self.stress_response_pattern +
    #         self.vulnerability_comfort_zone +
    #         self.empathy_style +
    #         self.emotional_recovery_pattern
    #     )
    

    # # Create all the getters for EmotionalDNA_PersonaScore
    # def get_initial_mood_assessment(self) -> float:
    #     """Get the initial mood assessment score."""
    #     return self.initial_mood_assessment
    
    # def set_initial_mood_assessment(self, value: float):
    #     """Set the initial mood assessment score."""
    #     self.initial_mood_assessment = value

    # def get_emotional_range_mapping(self) -> float:
    #     """Get the emotional range mapping score."""
    #     return self.emotional_range_mapping

    # def set_emotional_range_mapping(self, value: float):
    #     """Set the emotional range mapping score."""
    #     self.emotional_range_mapping = value    

    # def get_stress_response_pattern(self) -> float:
    #     """Get the stress response pattern score."""
    #     return self.stress_response_pattern
    
    # def set_stress_response_pattern(self, value: float):
    #     """Set the stress response pattern score."""
    #     self.stress_response_pattern = value

    # # Vulnerability comfort zone is a score that indicates how comfortable the persona is with vulnerability.
    # # It can be used to assess the persona's openness to emotional sharing and intimacy.
    # # This can be particularly useful in relationship dynamics and emotional support scenarios.
    # def get_vulnerability_comfort_zone(self) -> float:
    #     """Get the vulnerability comfort zone score."""
    #     return self.vulnerability_comfort_zone
    
    # def set_vulnerability_comfort_zone(self, value: float):
    #     """Set the vulnerability comfort zone score."""
    #     self.vulnerability_comfort_zone = value

    # # Create all the methods for EmotionalDNA_PersonaScore
    
    # # Empathy style is a score that indicates how empathetic the persona is in their interactions.
    # # It can be used to assess the persona's ability to understand and share the feelings of others.
    # # This can be particularly useful in relationship dynamics and emotional support scenarios.
    # def get_empathy_style(self) -> float:
    #     """Get the empathy style score."""
    #     return self.empathy_style

    # def set_empathy_style(self, value: float):
    #     """Set the empathy style score."""
    #     self.empathy_style = value

    # # Emotional recovery pattern is a score that indicates how well the persona recovers emotionally after stress or challenges.
    # # It can be used to assess the resilience and emotional stability of the persona.
    # def get_emotional_recovery_pattern(self) -> float:
    #     """Get the emotional recovery pattern score."""
    #     return self.emotional_recovery_pattern

    # def set_emotional_recovery_pattern(self, value: float):
    #     """Set the emotional recovery pattern score."""
    #     self.emotional_recovery_pattern = value

    # Instead of doing the above for all the classes, we can use a generic method to set the attributes
    # def set_attribute_score(self, attribute: str, value: float):
    #     """Set the score for a specific attribute."""
    #     if hasattr(self, attribute):
    #         setattr(self, attribute, value)
    #     else:
    #         raise ValueError(f"Attribute '{attribute}' does not exist in EmotionalDNA_PersonaScore.")

class CommunicationBlueprint_PersonaScore(PersonaScore):
    conflict_resolution_style: float
    conversation_rhythm: float
    humor_playfulness: float
    serious_discussion_approach: float
    love_language_expression: float

    # # Method to calculate the total score of all attributes
    # def total_attributes_score(self) -> float:
    #     """Calculate the total score of all attributes."""
    #     return (
    #         self.conflict_resolution_style +
    #         self.conversation_rhythm +
    #         self.humor_playfulness +
    #         self.serious_discussion_approach +
    #         self.love_language_expression
    #     )

    # def set_attribute_score(self, attribute: str, value: float):
    #     """Set the score for a specific attribute."""
    #     if hasattr(self, attribute):
    #         setattr(self, attribute, value)
    #     else:
    #         raise ValueError(f"Attribute '{attribute}' does not exist in CommunicationBlueprint_PersonaScore.")


class ValuesBeliefSystem_PersonaScore(PersonaScore):
    life_priorities_hierarchy: float
    ethical_decision_framework: float
    relationship_philosophy: float
    future_vision_clarity: float

    # # Method to calculate the total score of all attributes
    # def total_attributes_score(self) -> float:
    #     """Calculate the total score of all attributes."""
    #     return (
    #         self.life_priorities_hierarchy +
    #         self.ethical_decision_framework +
    #         self.relationship_philosophy +
    #         self.future_vision_clarity
    #     )

    # def set_attribute_score(self, attribute: str, value: float):
    #     """Set the score for a specific attribute."""
    #     if hasattr(self, attribute):
    #         setattr(self, attribute, value)
    #     else:
    #         raise ValueError(f"Attribute '{attribute}' does not exist in ValuesBeliefSystem_PersonaScore.")


class PersonalityAuthenticity_PersonaScore(PersonaScore):
    big_five_traits: float
    social_vs_private_self: float
    decision_making_style: float
    spontaneity_vs_planning: float

    # # Method to calculate the total score of all attributes
    # def total_attributes_score(self) -> float:
    #     """Calculate the total score of all attributes."""
    #     return (
    #         self.big_five_traits +
    #         self.social_vs_private_self +
    #         self.decision_making_style +
    #         self.spontaneity_vs_planning
    #     )

    # def set_attribute_score(self, attribute: str, value: float):
    #     """Set the score for a specific attribute."""
    #     if hasattr(self, attribute):
    #         setattr(self, attribute, value)
    #     else:
    #         raise ValueError(f"Attribute '{attribute}' does not exist in PersonalityAuthenticity_PersonaScore.")


class RelationshipReadiness_PersonaScore(PersonaScore):
    attachment_style_clarity: float
    compromise_flexibility: float
    intimacy_comfort_levels: float
    partnership_expectations: float

    # # Method to calculate the total score of all attributes
    # def total_attributes_score(self) -> float:
    #     """Calculate the total score of all attributes."""
    #     return (
    #         self.attachment_style_clarity +
    #         self.compromise_flexibility +
    #         self.intimacy_comfort_levels +
    #         self.partnership_expectations
    #     )

    # def set_attribute_score(self, attribute: str, value: float):
    #     """Set the score for a specific attribute."""
    #     if hasattr(self, attribute):
    #         setattr(self, attribute, value)
    #     else:
    #         raise ValueError(f"Attribute '{attribute}' does not exist in RelationshipReadiness_PersonaScore.")

    # @property
    # def attachment_style(self) -> float:
    #     """Get the attachment style clarity score."""
    #     return self.attachment_style_clarity

    # @attachment_style.setter
    # def attachment_style(self, value: float):
    #     """Set the attachment style clarity score."""
    #     self.attachment_style_clarity = value


class LifeCompatibilityMatrix_PersonaScore(PersonaScore):
    lifestyle_preferences: float
    financial_philosophy: float
    family_future_planning: float
    career_ambition_balance: float

    # Method to calculate the total score of all attributes
    # def total_attributes_score(self) -> float:
    #     """Calculate the total score of all attributes."""
    #     return (
    #         self.lifestyle_preferences +
    #         self.financial_philosophy +
    #         self.family_future_planning +
    #         self.career_ambition_balance
    #     )

    # def set_attribute_score(self, attribute: str, value: float):
    #     """Set the score for a specific attribute."""
    #     if hasattr(self, attribute):
    #         setattr(self, attribute, value)
    #     else:
    #         raise ValueError(f"Attribute '{attribute}' does not exist in LifeCompatibilityMatrix_PersonaScore.")


class GrowthChallengeThreshold_PersonaScore(PersonaScore):
    learning_style_preferences: float
    comfort_zone_expansion: float
    feedback_reception: float
    personal_development_drive: float

    # Method to calculate the total score of all attributes
    # def total_attributes_score(self) -> float:
    #     """Calculate the total score of all attributes."""
    #     return (
    #         self.learning_style_preferences +
    #         self.comfort_zone_expansion +
    #         self.feedback_reception +
    #         self.personal_development_drive
    #     )

    # def set_attribute_score(self, attribute: str, value: float):
    #     """Set the score for a specific attribute."""
    #     if hasattr(self, attribute):
    #         setattr(self, attribute, value)
    #     else:
    #         raise ValueError(f"Attribute '{attribute}' does not exist in GrowthChallengeThreshold_PersonaScore.")


class IntuitiveConnection_PersonaScore(PersonaScore):
    energy_vibe_patterns: float
    unspoken_needs_detection: float
    subtle_communication_cues: float
    emotional_resonance_frequency: float

    # Method to calculate the total score of all attributes
    # def total_attributes_score(self) -> float:
    #     """Calculate the total score of all attributes."""
    #     return (
    #         self.energy_vibe_patterns +
    #         self.unspoken_needs_detection +
    #         self.subtle_communication_cues +
    #         self.emotional_resonance_frequency
    #     )

    # def set_attribute_score(self, attribute: str, value: float):
    #     """Set the score for a specific attribute."""
    #     if hasattr(self, attribute):
    #         setattr(self, attribute, value)
    #     else:
    #         raise ValueError(f"Attribute '{attribute}' does not exist in IntuitiveConnection_PersonaScore.")

class PersonaScores(BaseModel):
    emotional_dna: EmotionalDNA_PersonaScore
    communication_blueprint: CommunicationBlueprint_PersonaScore
    values_belief_system: ValuesBeliefSystem_PersonaScore
    personality_authenticity: PersonalityAuthenticity_PersonaScore
    relationship_readiness: RelationshipReadiness_PersonaScore
    life_compatibility_matrix: LifeCompatibilityMatrix_PersonaScore
    growth_challenge_threshold: GrowthChallengeThreshold_PersonaScore
    intuitive_connection: IntuitiveConnection_PersonaScore

    # Get all dimensions as a list
    @property
    def dimensions(self) -> List[PersonaScore]:
        """Get all dimensions as a list."""
        return [
            self.emotional_dna,
            self.communication_blueprint,
            self.values_belief_system,
            self.personality_authenticity,
            self.relationship_readiness,
            self.life_compatibility_matrix,
            self.growth_challenge_threshold,
            self.intuitive_connection
        ]

    # def to_dict(self) -> Dict[str, Dict[str, float]]:
    #     return {field: value.dict() for field, value in self.model_dump().items()}    

    @classmethod
    def from_dict(cls, data: Dict[str, Dict[str, float]]) -> 'PersonaScores':
        return cls(
            emotional_dna=EmotionalDNA_PersonaScore(**data['emotional_dna']),
            communication_blueprint=CommunicationBlueprint_PersonaScore(**data['communication_blueprint']),
            values_belief_system=ValuesBeliefSystem_PersonaScore(**data['values_belief_system']),
            personality_authenticity=PersonalityAuthenticity_PersonaScore(**data['personality_authenticity']),
            relationship_readiness=RelationshipReadiness_PersonaScore(**data['relationship_readiness']),
            life_compatibility_matrix=LifeCompatibilityMatrix_PersonaScore(**data['life_compatibility_matrix']),
            growth_challenge_threshold=GrowthChallengeThreshold_PersonaScore(**data['growth_challenge_threshold']),
            intuitive_connection=IntuitiveConnection_PersonaScore(**data['intuitive_connection'])
        )
    
    def to_dict(self) -> Dict[str, Dict[str, float]]:
        """Convert PersonaScores to a dictionary."""
        return {
            "emotional_dna": self.emotional_dna.model_dump(),
            "communication_blueprint": self.communication_blueprint.model_dump(),
            "values_belief_system": self.values_belief_system.model_dump(),
            "personality_authenticity": self.personality_authenticity.model_dump(),
            "relationship_readiness": self.relationship_readiness.model_dump(),
            "life_compatibility_matrix": self.life_compatibility_matrix.model_dump(),
            "growth_challenge_threshold": self.growth_challenge_threshold.model_dump(),
            "intuitive_connection": self.intuitive_connection.model_dump()
        }
    
    def set_score(self, dimension: str, value: float):
        """Set the score for a specific dimension."""
        if hasattr(self, dimension):
            getattr(self, dimension).set_score(value)
        else:
            raise ValueError(f"Dimension '{dimension}' does not exist in PersonaScores.")
        
    def get_dimension(self, dimension: str) -> PersonaScore:
        """Get the score for a specific dimension."""
        if hasattr(self, dimension):
            return getattr(self, dimension)
        else:
            raise ValueError(f"Dimension '{dimension}' does not exist in PersonaScores.")