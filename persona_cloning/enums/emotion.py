# Emotion categories and intensities
from enum import Enum

class EmotionCategory(Enum):
    PRIMARY = "primary"  # joy, sadness, anger, fear, surprise, disgust
    SECONDARY = "secondary"  # guilt, shame, pride, envy, gratitude, hope
    SOCIAL = "social"  # empathy, compassion, admiration, contempt
    COMPLEX = "complex"  # nostalgia, melancholy, euphoria, ambivalence

class EmotionIntensity(Enum):
    SUBTLE = 1
    MILD = 2
    MODERATE = 3
    STRONG = 4
    INTENSE = 5

class EmotionClassifierLabel(Enum):
    ANGER = "anger"
    DISGUST = "disgust"
    FEAR = "fear"
    JOY = "joy"
    NEUTRAL = "neutral"
    SADNESS = "sadness"
    SURPRISE = "surprise"

class EmotionSentimentLabel(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"