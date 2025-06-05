from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from persona_cloning.enums.emotion import EmotionCategory, EmotionClassifierLabel, EmotionIntensity


@dataclass
class DetectedEmotion:
    name: str
    category: EmotionCategory
    intensity: EmotionIntensity
    confidence: float
    triggers: List[str] = field(default_factory=list)
    context_clues: List[str] = field(default_factory=list)

@dataclass
class EmotionalState:
    dominant_emotions: List[DetectedEmotion]
    emotional_complexity: float  # 0-1, higher = more mixed emotions
    emotional_stability: float   # 0-1, based on recent history
    transition_type: str        # gradual, sudden, cyclical, stable
    arousal_level: float        # 0-1, emotional activation
    valence: float             # -1 to 1, negative to positive
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class EmotionScore:
    label: EmotionClassifierLabel
    score: float