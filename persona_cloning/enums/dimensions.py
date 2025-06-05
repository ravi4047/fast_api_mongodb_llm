from enum import Enum

class Dimension(str, Enum):
    EMOTIONAL_DNA = "emotional_dna"
    COMMUNICATION_BLUEPRINT = "communication_blueprint"
    VALUES_BELIFE_SYSTEM = "values_belief_system"
    PERSONALITY_AUTHENTICITY = "personality_authenticity"
    RELATIONSHIP_READINESS = "relationship_readiness"
    LIFE_COMPATIBILITY_MATRIX = "life_compatibility_matrix"
    GROWTH_CHALLENGE_THRESHOLD = "growth_challenge_threshold"
    INTUITIVE_CONNECTION = "intuitive_connection"

class EmotionalDNA(str, Enum):
    INITIAL_MOOD_ASSESSMENT = "initial_mood_assessment"
    EMOTIONAL_RANGE_MAPPING = "emotional_range_mapping"
    STRESS_RESPONSE_PATTERN = "stress_response_pattern"
    VULNERABILITY_COMFORT_ZONE = "vulnerability_comfort_zone"
    EMPATHY_STYLE = "empathy_style"
    EMOTIONAL_RECOVERY_PATTERN = "emotional_recovery_pattern"
    
class CommunicationBlueprint(str, Enum):
    INITIAL_COMMUNICATION_STYLE = "initial_communication_style"
    PREFERRED_CHANNELS = "preferred_channels"
    CONFLICT_RESOLUTION_STYLE = "conflict_resolution_style"
    ACTIVE_LISTENING_TENDENCIES = "active_listening_tendencies"
    NONVERBAL_COMMUNICATION_STYLE = "nonverbal_communication_style"
    FEEDBACK_RECEPTIVITY = "feedback_receptivity"

class ValuesBeliefSystem(str, Enum):
    CORE_VALUES = "core_values"
    BELIEF_IN_RELATIONSHIPS = "belief_in_relationships"
    LIFE_PRIORITIES = "life_priorities"
    ETHICAL_STANDARDS = "ethical_standards"
    SPIRITUAL_ORIENTATION = "spiritual_orientation"
    SOCIAL_RESPONSIBILITY = "social_responsibility"

class PersonalityAuthenticity(str, Enum):
    CORE_PERSONALITY_TRAITS = "core_personality_traits"
    PERSONALITY_FLEXIBILITY = "personality_flexibility"
    AUTHENTICITY_IN_INTERACTIONS = "authenticity_in_interactions"
    SELF_AWARENESS_LEVEL = "self_awareness_level"
    PERSONALITY_CONSISTENCY = "personality_consistency"
    ADAPTABILITY_TO_CHANGE = "adaptability_to_change"

class RelationshipReadiness(str, Enum):
    CURRENT_RELATIONSHIP_STATUS = "current_relationship_status"
    PAST_RELATIONSHIP_EXPERIENCES = "past_relationship_experiences"
    DESIRED_RELATIONSHIP_TYPE = "desired_relationship_type"
    COMMITMENT_LEVEL = "commitment_level"
    TRUST_ISSUES = "trust_issues"
    RELATIONSHIP_GOALS = "relationship_goals"

class LifeCompatibilityMatrix(str, Enum):
    LIFE_STYLE_COMPATIBILITY = "life_style_compatibility"
    FUTURE_PLANS_ALIGNMENT = "future_plans_alignment"
    FAMILY_PLANNING_VIEWS = "family_planning_views"
    CAREER_AMBITIONS = "career_ambitions"
    FINANCIAL_COMPATIBILITY = "financial_compatibility"
    HOBBIES_AND_INTERESTS = "hobbies_and_interests"

class GrowthChallengeThreshold(str, Enum):
    CURRENT_GROWTH_CHALLENGE_LEVEL = "current_growth_challenge_level"
    PREFERRED_CHALLENGE_INTENSITY = "preferred_challenge_intensity"
    STRESS_TOLERANCE = "stress_tolerance"
    RESILIENCE_CAPACITY = "resilience_capacity"
    GROWTH_MINDSET = "growth_mindset"
    ADAPTABILITY_TO_CHANGES = "adaptability_to_changes"

class IntuitiveConnection(str, Enum):
    INITIAL_INTUITIVE_CONNECTION = "initial_intuitive_connection"
    INTUITIVE_FEEDBACK_RECEPTIVITY = "intuitive_feedback_receptivity"
    SYNCHRONICITY_SENSITIVITY = "synchronicity_sensitivity"
    INTUITIVE_DECISION_MAKING_STYLE = "intuitive_decision_making_style"
    SPIRITUAL_OR_INTUITIVE_BELIEFS = "spiritual_or_intuitive_beliefs"
    DEEP_CONNECTION_EXPERIENCES = "deep_connection_experiences"