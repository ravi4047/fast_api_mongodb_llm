from enum import Enum, auto

# https://www.perplexity.ai/search/i-am-creating-a-chatbot-for-da-G6jBs1pCQiWn_GDqu_t4ww

# 1. Emotional DNA Score (0-100)
# Emotional Range Mapping (15 points) - How you express joy, sadness, anger, fear, excitement

# Stress Response Pattern (20 points) - How you handle pressure, conflict, disappointment

# Vulnerability Comfort Zone (25 points) - When/how you open up emotionally

# Empathy Style (20 points) - How you give and receive emotional support

# Emotional Recovery Pattern (20 points) - How you bounce back from setbacks

# 2. Communication Blueprint Score (0-100)
# Conflict Resolution Style (25 points) - How you handle disagreements

# Conversation Rhythm (20 points) - Your preferred pace, depth, topics

# Humor & Playfulness (15 points) - What makes you laugh, your wit style

# Serious Discussion Approach (20 points) - How you handle deep topics

# Love Language Expression (20 points) - How you show and receive affection

# 3. Values & Belief System Score (0-100)
# Life Priorities Hierarchy (30 points) - Career, family, growth, adventure priorities

# Ethical Decision Framework (25 points) - Your moral compass in tough situations

# Relationship Philosophy (25 points) - What you believe makes relationships work

# Future Vision Clarity (20 points) - Your dreams and long-term goals

# 4. Personality Authenticity Score (0-100)
# Big Five Personality Traits (30 points) - Openness, conscientiousness, extraversion, agreeableness, neuroticism

# Social vs Private Self (25 points) - How you differ in public vs intimate settings

# Decision-Making Style (20 points) - Analytical, intuitive, collaborative approaches

# Spontaneity vs Planning (25 points) - How you approach life choices

# 5. Relationship Readiness Score (0-100)
# Attachment Style Clarity (30 points) - Secure, anxious, avoidant patterns

# Compromise & Flexibility (25 points) - How you handle relationship negotiations

# Intimacy Comfort Levels (25 points) - Physical, emotional, intellectual intimacy

# Partnership Expectations (20 points) - What you need vs what you give

# 6. Life Compatibility Matrix Score (0-100)
# Lifestyle Preferences (25 points) - Daily routines, social needs, alone time

# Financial Philosophy (20 points) - Money attitudes, spending, saving, goals

# Family & Future Planning (30 points) - Kids, marriage, family involvement

# Career & Ambition Balance (25 points) - Work-life balance, ambition level

# 7. Growth & Challenge Threshold Score (0-100)
# Learning Style Preferences (20 points) - How you like to grow and develop

# Comfort Zone Expansion (25 points) - How you handle new experiences

# Feedback Reception (25 points) - How you handle criticism and suggestions

# Personal Development Drive (30 points) - Your motivation for self-improvement

# 8. Intuitive Connection Score (0-100)
# Energy & Vibe Patterns (25 points) - Your natural energy levels and rhythms

# Unspoken Needs Detection (30 points) - What you need but don't always say

# Subtle Communication Cues (25 points) - Your non-verbal communication style

# Emotional Resonance Frequency (20 points) - What emotional wavelength you operate on

# Each dimension totals 100 points across its specific areas, and the overall Persona Clone Completion Score is calculated using weighted averages with different importance levels for each dimension.
    

# class Dimension(str, Enum):
#     EMOTIONAL_DNA = "emotional_dna"
#     COMMUNICATION_BLUEPRINT = "communication_blueprint"
#     VALUES_BELIFE_SYSTEM = "values_belief_system"
#     PERSONALITY_AUTHENTICITY = "personality_authenticity"
#     RELATIONSHIP_READINESS = "relationship_readiness"
#     LIFE_COMPATIBILITY_MATRIX = "life_compatibility_matrix"
#     GROWTH_CHALLENGE_THRESHOLD = "growth_challenge_threshold"
#     INTUITIVE_CONNECTION = "intuitive_connection"

# class Phase(str, Enum):
#     MIRROR_PHASE = "mirror_phase"
#     GENTLE_CHALLENGER = "gentle_challenger"
#     COMPLEMENTARY_OPPOSITE = "complementary_opposite"
#     GROWTH_CATALYST = "growth_catalyst"
#     AUTHENTIC_COMPANION = "authentic_companion"


# class EmotionalDNA_SpecificArea(str, Enum):
#     INITIAL_MOOD_ASSESSMENT = "initial_mood_assessment"

#### Personality --------------------

### Personality's Emoji Usage
class EmojiUsage(str, Enum):
    FREQUENT_AND_CONTEXTUAL = "frequent_and_contextual"
    SELECTIVE_AND_MEANINGFUL = "selective_and_meaningful"

    ### 📝 Todo To be more added
    MINIMUM = "minimum"

class PersonalityTraits(str, Enum):
    NURTURING = "nurturing"
    PLAYFUL = "playful"
    EMOTIONALLY_INTELLIGENT = "emotionally_intelligent"
    SUPPORTIVE = "supportive"

    PROTECTIVE = "protective"
    UNDERSTANDING = "understanding"
    CONFIDENT = "confident"
    CARING = "caring"
    # Add more traits as needed

class CommunicationStyle(str, Enum):
    WARM_AND_ENCOURAGING = "warm_and_encouraging"
    REASSURING_AND_STRONG = "reassuring_and_strong"

    ### 📝 Todo To be more added
    GENTLE_AND_GRADUAL = "gentle_and_gradual"
    STEADY_AND_PATIENT = "steady_and_patient"

class AffectionExpressions(str, Enum):
    SWEETIE = "sweetie"
    LOVE = "love"
    BABE = "babe"
    DARLING = "darling"

    BEAUTIFUL = "beautiful"
    GORGEOUS = "gorgeous"
    SWEETHEART = "sweetheart"
    PRINCESS = "princess"

class VulnerabilityApproach(str, Enum):
    GENTLE_AND_GRADUAL = "gentle_and_gradual"
    STEADY_AND_PATIENT = "steady_and_patient"

    ### 📝 Todo To be more added
    GRADUAL = "gradual"
    PATIENT = "patient"

class HumorStyle(str, Enum):
    LIGHT_TEASING_AND_WORDPLAY = "light_teasing_and_wordplay"
    GENTLE_TEASING_AND_CHARM = "gentle_teasing_and_charm"

    ### 📝 Todo To be more added
    CHARMING = "charming"
    WITTY = "witty"

class AvatarName(Enum):
    EMMA = "Emma"
    ALEX = "Alex"

    ### 📝 Todo To be more added
    JESSICA = "Jessica"
    MICHAEL = "Michael"
    SOPHIA = "Sophia"
    DAVID = "David"
    OLIVIA = "Olivia"
    JAMES = "James"
    ISABELLA = "Isabella"
    CHARLIE = "Charlie"
    LILY = "Lily"
    BENJAMIN = "Benjamin"
    MIA = "Mia"
    NOAH = "Noah"


# class Phase