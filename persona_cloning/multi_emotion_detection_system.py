from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional, Tuple
import numpy as np
import re
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import asyncio
from transformers.pipelines import pipeline
from transformers.models.auto.tokenization_auto import AutoTokenizer
from transformers.models.auto.modeling_auto import AutoModelForSequenceClassification
import torch
from collections import Counter, defaultdict, deque
import json

from persona_cloning.config.traits import Big5TraitsModel
from persona_cloning.emotion_handler import EmotionHandler
from persona_cloning.enums.emotion import EmotionCategory, EmotionIntensity
from persona_cloning.models.emotion import DetectedEmotion, EmotionalState


# https://claude.ai/chat/68d92fd3-0ce3-495d-a138-7e055256434d

# Initialize FastAPI app
app = FastAPI(title="Multi-Emotion Detection API", version="1.0.0")

# # Emotion categories and intensities
# class EmotionCategory(Enum):
#     PRIMARY = "primary"  # joy, sadness, anger, fear, surprise, disgust
#     SECONDARY = "secondary"  # guilt, shame, pride, envy, gratitude, hope
#     SOCIAL = "social"  # empathy, compassion, admiration, contempt
#     COMPLEX = "complex"  # nostalgia, melancholy, euphoria, ambivalence

# class EmotionIntensity(Enum):
#     SUBTLE = 1
#     MILD = 2
#     MODERATE = 3
#     STRONG = 4
#     INTENSE = 5

# @dataclass
# class DetectedEmotion:
#     name: str
#     category: EmotionCategory
#     intensity: EmotionIntensity
#     confidence: float
#     triggers: List[str] = field(default_factory=list)
#     context_clues: List[str] = field(default_factory=list)

# @dataclass
# class EmotionalState:
#     dominant_emotions: List[DetectedEmotion]
#     emotional_complexity: float  # 0-1, higher = more mixed emotions
#     emotional_stability: float   # 0-1, based on recent history
#     transition_type: str        # gradual, sudden, cyclical, stable
#     arousal_level: float        # 0-1, emotional activation
#     valence: float             # -1 to 1, negative to positive
#     timestamp: datetime = field(default_factory=datetime.now)

class EmotionDetector:
    def __init__(self):
        # Initialize lightweight models for CPU inference
        self.emotion_classifier = None
        self.sentiment_analyzer = None
        # self.load_models() ## Not needed
        
        # Emotion lexicons and patterns
        self.emotion_lexicon = self._build_emotion_lexicon()
        self.intensity_modifiers = self._build_intensity_modifiers()
        self.contextual_patterns = self._build_contextual_patterns()
        
        # User emotion history (in-memory for demo, use Redis/DB in production)
        # self.user_emotion_history = defaultdict(lambda: deque(maxlen=50))
        self.user_emotion_history: defaultdict[str, deque[dict]] = defaultdict(lambda: deque(maxlen=50))
        self.user_baselines = defaultdict(dict)
    
    # We can't do it like this. You need to load the models nicely and outside the init method.

    ### ❌❌ Unused code, but kept for reference
    def load_models(self):
        """Load lightweight models optimized for CPU"""
        try:
            # Using DistilBERT for efficiency
            model_name = "j-hartmann/emotion-english-distilroberta-base"
            self.emotion_classifier = pipeline(
                "text-classification",
                model=model_name,
                device=-1,  # CPU
                return_all_scores=True
            )
            
            # Sentiment for valence calculation
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                device=-1,
                return_all_scores=True
            )
        except Exception as e:
            print(f"Model loading failed: {e}")
            # Fallback to rule-based approach
            self.emotion_classifier = None
            self.sentiment_analyzer = None
    
    def _build_emotion_lexicon(self) -> Dict[str, Dict]:
        """Comprehensive emotion lexicon with context sensitivity"""
        return {
            # Primary emotions
            "joy": {
                "keywords": ["happy", "excited", "thrilled", "delighted", "elated", "cheerful", "jubilant"],
                "patterns": [r"\b(so|really|very)\s+(happy|excited)", r"can't\s+wait", r"love\s+it"],
                "category": EmotionCategory.PRIMARY,
                "valence": 0.8
            },
            "sadness": {
                "keywords": ["sad", "depressed", "down", "blue", "melancholy", "dejected", "despondent"],
                "patterns": [r"feel(ing)?\s+(down|low)", r"can't\s+help\s+but\s+cry", r"everything\s+seems"],
                "category": EmotionCategory.PRIMARY,
                "valence": -0.7
            },
            "anger": {
                "keywords": ["angry", "furious", "mad", "irritated", "frustrated", "livid", "enraged"],
                "patterns": [r"so\s+(mad|angry)", r"can't\s+believe", r"this\s+is\s+ridiculous"],
                "category": EmotionCategory.PRIMARY,
                "valence": -0.6
            },
            "fear": {
                "keywords": ["scared", "afraid", "terrified", "anxious", "worried", "nervous", "panicked"],
                "patterns": [r"what\s+if", r"afraid\s+that", r"worried\s+about"],
                "category": EmotionCategory.PRIMARY,
                "valence": -0.5
            },
            "surprise": {
                "keywords": ["surprised", "shocked", "amazed", "astonished", "stunned", "bewildered"],
                "patterns": [r"didn't\s+expect", r"never\s+thought", r"out\s+of\s+nowhere"],
                "category": EmotionCategory.PRIMARY,
                "valence": 0.1
            },
            "disgust": {
                "keywords": ["disgusted", "revolted", "repulsed", "sickened", "appalled"],
                "patterns": [r"makes\s+me\s+sick", r"can't\s+stand", r"absolutely\s+hate"],
                "category": EmotionCategory.PRIMARY,
                "valence": -0.8
            },
            
            # Secondary emotions
            "guilt": {
                "keywords": ["guilty", "ashamed", "regret", "remorse", "sorry"],
                "patterns": [r"should\s+have", r"if\s+only", r"feel\s+bad\s+about"],
                "category": EmotionCategory.SECONDARY,
                "valence": -0.6
            },
            "pride": {
                "keywords": ["proud", "accomplished", "achieved", "succeeded"],
                "patterns": [r"proud\s+of", r"finally\s+did", r"worked\s+so\s+hard"],
                "category": EmotionCategory.SECONDARY,
                "valence": 0.7
            },
            "envy": {
                "keywords": ["jealous", "envious", "wish\s+I\s+had"],
                "patterns": [r"why\s+can't\s+I", r"they\s+have\s+everything", r"not\s+fair"],
                "category": EmotionCategory.SECONDARY,
                "valence": -0.4
            },
            "gratitude": {
                "keywords": ["grateful", "thankful", "appreciate", "blessed"],
                "patterns": [r"thank\s+you\s+for", r"so\s+grateful", r"appreciate\s+that"],
                "category": EmotionCategory.SECONDARY,
                "valence": 0.6
            },
            "hope": {
                "keywords": ["hopeful", "optimistic", "looking\s+forward", "excited\s+about"],
                "patterns": [r"can't\s+wait\s+for", r"hopefully", r"things\s+will\s+get\s+better"],
                "category": EmotionCategory.SECONDARY,
                "valence": 0.5
            },
            
            # Social emotions
            "empathy": {
                "keywords": ["understand", "feel\s+for", "sorry\s+to\s+hear"],
                "patterns": [r"I\s+understand", r"must\s+be\s+hard", r"feel\s+for\s+you"],
                "category": EmotionCategory.SOCIAL,
                "valence": 0.2
            },
            "compassion": {
                "keywords": ["care\s+about", "concerned\s+for", "want\s+to\s+help"],
                "patterns": [r"here\s+if\s+you\s+need", r"care\s+about\s+you", r"want\s+to\s+help"],
                "category": EmotionCategory.SOCIAL,
                "valence": 0.4
            },
            
            # Complex emotions
            "nostalgia": {
                "keywords": ["nostalgic", "remember\s+when", "miss\s+the\s+old"],
                "patterns": [r"back\s+in\s+the\s+day", r"wish\s+we\s+could\s+go\s+back", r"those\s+were\s+the\s+days"],
                "category": EmotionCategory.COMPLEX,
                "valence": 0.1
            },
            "ambivalence": {
                "keywords": ["mixed\s+feelings", "torn\s+between", "don't\s+know\s+how"],
                "patterns": [r"on\s+one\s+hand.*on\s+the\s+other", r"part\s+of\s+me.*but", r"conflicted"],
                "category": EmotionCategory.COMPLEX,
                "valence": 0.0
            }
        }
    
    def _build_intensity_modifiers(self) -> Dict[str, float]:
        """Words that modify emotional intensity"""
        return {
            # Amplifiers
            "extremely": 2.0, "incredibly": 1.8, "absolutely": 1.7, "completely": 1.6,
            "totally": 1.5, "really": 1.4, "very": 1.3, "quite": 1.2, "pretty": 1.1,
            
            # Diminishers
            "slightly": 0.7, "somewhat": 0.8, "a bit": 0.6, "kind of": 0.7,
            "sort of": 0.7, "rather": 0.9, "fairly": 0.9, "maybe": 0.5,
            
            # Hedges
            "I guess": 0.6, "I think": 0.8, "perhaps": 0.7, "possibly": 0.6
        }
    
    def _build_contextual_patterns(self) -> Dict[str, List[str]]:
        """Context patterns that affect emotion interpretation"""
        return {
            "negation": [r"not\s+", r"never\s+", r"don't\s+", r"can't\s+", r"won't\s+"],
            "uncertainty": [r"maybe\s+", r"perhaps\s+", r"might\s+", r"could\s+be"],
            "temporal": [r"used\s+to\s+", r"will\s+be\s+", r"going\s+to\s+", r"about\s+to\s+"],
            "conditional": [r"if\s+", r"when\s+", r"unless\s+", r"suppose\s+"],
            "comparison": [r"more\s+.*than", r"less\s+.*than", r"as\s+.*as", r"compared\s+to"]
        }
    
    async def detect_emotions(self, text: str, user_id: str|None = None) -> List[DetectedEmotion]:
        """Main emotion detection method combining multiple approaches"""
        emotions = []
        
        # Approach 1: Model-based detection (if available)
        if self.emotion_classifier:
            model_emotions = await self._model_based_detection(text)
            emotions.extend(model_emotions)
        
        # Approach 2: Lexicon-based detection
        lexicon_emotions = await self._lexicon_based_detection(text)
        emotions.extend(lexicon_emotions)
        
        # Approach 3: Pattern-based detection
        pattern_emotions = await self._pattern_based_detection(text)
        emotions.extend(pattern_emotions)
        
        # Merge and deduplicate emotions
        merged_emotions = self._merge_emotions(emotions)
        
        # Apply contextual adjustments
        adjusted_emotions = self._apply_contextual_adjustments(merged_emotions, text)
        
        # Filter by confidence threshold
        filtered_emotions = [e for e in adjusted_emotions if e.confidence > 0.3]
        
        # Sort by confidence
        filtered_emotions.sort(key=lambda x: x.confidence, reverse=True)
        
        return filtered_emotions[:5]  # Top 5 emotions
    
    async def _model_based_detection(self, text: str) -> List[DetectedEmotion]:
        """Use transformer model for emotion detection"""
        emotions = []
        try:
            # results = self.emotion_classifier(text)
            results = emotion_detector.emotion_classifier(text)
            for result in results[0]:  # results is list of lists
                if result['score'] > 0.1:  # Threshold for inclusion
                    emotion_name = result['label'].lower()
                    intensity = self._score_to_intensity(result['score'])
                    
                    emotion = DetectedEmotion(
                        name=emotion_name,
                        category=self._get_emotion_category(emotion_name),
                        intensity=intensity,
                        confidence=result['score'],
                        triggers=[],
                        context_clues=[]
                    )
                    emotions.append(emotion)
        except Exception as e:
            print(f"Model-based detection failed: {e}")
        
        return emotions
    
    async def _lexicon_based_detection(self, text: str) -> List[DetectedEmotion]:
        """Detect emotions using keyword matching"""
        emotions = []
        text_lower = text.lower()
        
        for emotion_name, emotion_data in self.emotion_lexicon.items():
            matches = []
            base_score = 0.0
            
            # Keyword matching
            for keyword in emotion_data["keywords"]:
                if re.search(r'\b' + keyword + r'\b', text_lower):
                    matches.append(keyword)
                    base_score += 0.3
            
            # Pattern matching
            for pattern in emotion_data["patterns"]:
                if re.search(pattern, text_lower):
                    matches.append(f"pattern: {pattern}")
                    base_score += 0.4
            
            if base_score > 0:
                # Apply intensity modifiers
                intensity_score = self._calculate_intensity(text_lower, base_score)
                
                emotion = DetectedEmotion(
                    name=emotion_name,
                    category=emotion_data["category"],
                    intensity=self._score_to_intensity(intensity_score),
                    confidence=min(intensity_score, 0.95),
                    triggers=matches,
                    context_clues=[]
                )
                emotions.append(emotion)
        
        return emotions
    
    async def _pattern_based_detection(self, text: str) -> List[DetectedEmotion]:
        """Detect emotions using advanced patterns and context"""
        emotions = []
        
        # Question patterns (often indicate confusion, curiosity, or anxiety)
        if re.search(r'\?.*\?', text) or text.count('?') > 2:
            emotion = DetectedEmotion(
                name="confusion",
                category=EmotionCategory.PRIMARY,
                intensity=EmotionIntensity.MILD,
                confidence=0.6,
                triggers=["multiple questions"],
                context_clues=["question pattern"]
            )
            emotions.append(emotion)
        
        # Exclamation patterns (excitement, surprise, anger)
        exclamation_count = text.count('!')
        if exclamation_count > 1:
            intensity = min(exclamation_count * 0.2 + 0.4, 0.9)
            emotion = DetectedEmotion(
                name="excitement",
                category=EmotionCategory.PRIMARY,
                intensity=self._score_to_intensity(intensity),
                confidence=intensity,
                triggers=[f"{exclamation_count} exclamations"],
                context_clues=["exclamation pattern"]
            )
            emotions.append(emotion)
        
        # Capitalization patterns (strong emotions)
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        if caps_ratio > 0.3:
            emotion = DetectedEmotion(
                name="intensity",
                category=EmotionCategory.COMPLEX,
                intensity=self._score_to_intensity(caps_ratio * 2),
                confidence=0.7,
                triggers=["high capitalization"],
                context_clues=["caps pattern"]
            )
            emotions.append(emotion)
        
        return emotions
    
    def _calculate_intensity(self, text: str, base_score: float) -> float:
        """Calculate emotion intensity based on modifiers"""
        intensity = base_score
        
        for modifier, multiplier in self.intensity_modifiers.items():
            if modifier in text:
                intensity *= multiplier
        
        # Check for repetition (indicates emphasis)
        words = text.split()
        word_counts = defaultdict(int)
        for word in words:
            word_counts[word] += 1
        
        max_repetition = max(word_counts.values()) if word_counts else 1
        if max_repetition > 1:
            intensity *= (1 + 0.1 * max_repetition)
        
        return min(intensity, 1.0)
    
    def _merge_emotions(self, emotions: List[DetectedEmotion]) -> List[DetectedEmotion]:
        """Merge duplicate emotions and combine their evidence"""
        emotion_dict = {}
        
        for emotion in emotions:
            if emotion.name in emotion_dict:
                existing = emotion_dict[emotion.name]
                # Combine confidence scores
                combined_confidence = (existing.confidence + emotion.confidence) / 2
                # Take higher intensity
                combined_intensity = max(existing.intensity, emotion.intensity)
                # Combine triggers and context clues
                combined_triggers = list(set(existing.triggers + emotion.triggers))
                combined_context = list(set(existing.context_clues + emotion.context_clues))
                
                emotion_dict[emotion.name] = DetectedEmotion(
                    name=emotion.name,
                    category=emotion.category,
                    intensity=combined_intensity,
                    confidence=combined_confidence,
                    triggers=combined_triggers,
                    context_clues=combined_context
                )
            else:
                emotion_dict[emotion.name] = emotion
        
        return list(emotion_dict.values())
    
    def _apply_contextual_adjustments(self, emotions: List[DetectedEmotion], text: str) -> List[DetectedEmotion]:
        """Apply contextual adjustments to emotion detection"""
        text_lower = text.lower()
        
        # Check for negation
        for pattern in self.contextual_patterns["negation"]:
            if re.search(pattern, text_lower):
                for emotion in emotions:
                    # Reduce confidence for negated emotions
                    emotion.confidence *= 0.7
                    emotion.context_clues.append("negation detected")
        
        # Check for uncertainty
        for pattern in self.contextual_patterns["uncertainty"]:
            if re.search(pattern, text_lower):
                for emotion in emotions:
                    if emotion.intensity.value > 2:
                        emotion.intensity = EmotionIntensity(emotion.intensity.value - 1)
                    emotion.context_clues.append("uncertainty detected")
        
        return emotions
    
    def _score_to_intensity(self, score: float) -> EmotionIntensity:
        """Convert confidence score to intensity enum"""
        if score < 0.2:
            return EmotionIntensity.SUBTLE
        elif score < 0.4:
            return EmotionIntensity.MILD
        elif score < 0.6:
            return EmotionIntensity.MODERATE
        elif score < 0.8:
            return EmotionIntensity.STRONG
        else:
            return EmotionIntensity.INTENSE
    
    def _get_emotion_category(self, emotion_name: str) -> EmotionCategory:
        """Get emotion category for unknown emotions"""
        if emotion_name in self.emotion_lexicon:
            return self.emotion_lexicon[emotion_name]["category"]
        return EmotionCategory.PRIMARY  # Default
    
    async def analyze_emotional_state(self, text: str, user_id: str) -> EmotionalState:
        """Comprehensive emotional state analysis"""
        emotions = await self.detect_emotions(text, user_id)
        
        if not emotions:
            return EmotionalState(
                dominant_emotions=[],
                emotional_complexity=0.0,
                emotional_stability=1.0,
                transition_type="stable",
                arousal_level=0.0,
                valence=0.0
            )
        
        # Calculate complexity (number of different emotions)
        complexity = min(len(emotions) / 5.0, 1.0)
        
        # Calculate valence (overall positivity/negativity)
        valence_sum = 0
        for emotion in emotions:
            if emotion.name in self.emotion_lexicon:
                valence_sum += self.emotion_lexicon[emotion.name]["valence"] * emotion.confidence
        valence = valence_sum / len(emotions) if emotions else 0.0
        
        # Calculate arousal (emotional activation)
        arousal = sum(emotion.intensity.value * emotion.confidence for emotion in emotions) / (5 * len(emotions))
        
        # Determine stability and transition type
        stability, transition_type = self._analyze_stability(user_id, emotions)
        
        # Store in history
        if user_id:
            self.user_emotion_history[user_id].append({
                'timestamp': datetime.now(),
                'emotions': emotions,
                'valence': valence,
                'arousal': arousal
            })
        
        return EmotionalState(
            dominant_emotions=emotions[:3],  # Top 3 emotions
            emotional_complexity=complexity,
            emotional_stability=stability,
            transition_type=transition_type,
            arousal_level=arousal,
            valence=valence
        )
    
    def _analyze_stability(self, user_id: str, current_emotions: List[DetectedEmotion]) -> Tuple[float, str]:
        """Analyze emotional stability based on history"""
        if not user_id or user_id not in self.user_emotion_history:
            return 1.0, "stable"
        
        history = list(self.user_emotion_history[user_id])
        if len(history) < 3:
            return 0.8, "stable"
        
        # Calculate stability based on emotional variance
        recent_valences = [entry['valence'] for entry in history[-5:]]
        recent_arousals = [entry['arousal'] for entry in history[-5:]]
        
        valence_variance = np.var(recent_valences) if len(recent_valences) > 1 else 0
        arousal_variance = np.var(recent_arousals) if len(recent_arousals) > 1 else 0
        
        # Combined stability score (lower variance = higher stability)
        stability = max(0.0, 1.0 - (valence_variance + arousal_variance) / 2)
        
        # Determine transition type
        if stability > 0.8:
            transition_type = "stable"
        elif valence_variance > arousal_variance:
            transition_type = "gradual"
        elif len(set(recent_valences[-3:])) == 3:  # All different
            transition_type = "sudden"
        else:
            transition_type = "cyclical"
        
        return stability, transition_type

# Initialize the emotion detector
emotion_detector = EmotionDetector()

# Pydantic models for API
class EmotionRequest(BaseModel):
    text: str
    # user_id: Optional[str] = None
    user_id: str
    include_history: bool = False

class EmotionResponse(BaseModel):
    emotions: List[Dict]
    emotional_state: Dict
    processing_time_ms: float

class ChatMessage(BaseModel):
    text: str
    user_id: str
    timestamp: Optional[datetime] = None

class PersonaUpdate(BaseModel):
    user_id: str
    emotional_insights: Dict
    relationship_dynamics: Dict
    growth_indicators: Dict

# API Endpoints
@app.post("/detect_emotions", response_model=EmotionResponse)
async def detect_emotions_endpoint(request: EmotionRequest):
    """Detect emotions in text with comprehensive analysis"""
    start_time = asyncio.get_event_loop().time()

    user_id = request.user_id if request.user_id else "anonymous"
    
    try:
        # Get emotional state analysis
        emotional_state = await emotion_detector.analyze_emotional_state(
            request.text, 
            user_id
        )
        
        # Convert to serializable format
        emotions_dict = [
            {
                "name": emotion.name,
                "category": emotion.category.value,
                "intensity": emotion.intensity.value,
                "confidence": emotion.confidence,
                "triggers": emotion.triggers,
                "context_clues": emotion.context_clues
            }
            for emotion in emotional_state.dominant_emotions
        ]
        
        emotional_state_dict = {
            "emotional_complexity": emotional_state.emotional_complexity,
            "emotional_stability": emotional_state.emotional_stability,
            "transition_type": emotional_state.transition_type,
            "arousal_level": emotional_state.arousal_level,
            "valence": emotional_state.valence,
            "timestamp": emotional_state.timestamp.isoformat()
        }
        
        # Include history if requested
        if request.include_history and request.user_id:
            history = list(emotion_detector.user_emotion_history[request.user_id])
            emotional_state_dict["recent_history"] = [
                {
                    "timestamp": entry["timestamp"].isoformat(),
                    "emotions": [e.name for e in entry["emotions"]],
                    "valence": entry["valence"],
                    "arousal": entry["arousal"]
                }
                for entry in history[-10:]  # Last 10 entries
            ]
        
        processing_time = (asyncio.get_event_loop().time() - start_time) * 1000
        
        return EmotionResponse(
            emotions=emotions_dict,
            emotional_state=emotional_state_dict,  
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Emotion detection failed: {str(e)}")

@app.post("/analyze_conversation")
async def analyze_conversation(messages: List[ChatMessage]):
    """Analyze emotional flow in a conversation"""
    try:
        conversation_analysis = {
            "emotional_journey": [],
            "dominant_themes": [],
            "emotional_peaks": [],
            "stability_analysis": {},
            "recommendations": []
        }
        
        for message in messages:
            emotional_state = await emotion_detector.analyze_emotional_state(
                message.text, 
                message.user_id
            )
            
            conversation_analysis["emotional_journey"].append({
                "timestamp": message.timestamp.isoformat() if message.timestamp else datetime.now().isoformat(),
                "user_id": message.user_id,
                "emotions": [e.name for e in emotional_state.dominant_emotions],
                "valence": emotional_state.valence,
                "arousal": emotional_state.arousal_level,
                "complexity": emotional_state.emotional_complexity
            })
        
        # Analyze patterns
        if conversation_analysis["emotional_journey"]:
            valences = [entry["valence"] for entry in conversation_analysis["emotional_journey"]]
            arousals = [entry["arousal"] for entry in conversation_analysis["emotional_journey"]]
            
            conversation_analysis["stability_analysis"] = {
                "valence_trend": "positive" if valences[-1] > valences[0] else "negative",
                "arousal_trend": "increasing" if arousals[-1] > arousals[0] else "decreasing",
                "volatility": float(np.std(valences)) if len(valences) > 1 else 0.0
            }
            
            # Generate recommendations for persona chatbot
            if conversation_analysis["stability_analysis"]["volatility"] > 0.5:
                conversation_analysis["recommendations"].append("High emotional volatility detected - consider stabilizing responses")
            
            if valences[-1] < -0.3:
                conversation_analysis["recommendations"].append("Negative emotional state - implement supportive conversation patterns")
        
        return conversation_analysis
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversation analysis failed: {str(e)}")

@app.post("/update_persona")
async def update_persona(update: PersonaUpdate):
    """Update persona model based on emotional insights"""
    try:
        # This would integrate with your persona model
        # For now, we'll return analysis for persona building
        
        user_history = list(emotion_detector.user_emotion_history[update.user_id])
        
        if not user_history:
            return {"message": "No emotional history available for persona update"}
        
        # Analyze patterns for persona building
        persona_insights = {
            "emotional_baseline": {
                "typical_valence": float(np.mean([entry["valence"] for entry in user_history])),
                "typical_arousal": float(np.mean([entry["arousal"] for entry in user_history])),
                "emotional_range": float(np.ptp([entry["valence"] for entry in user_history]))
            },
            "dominant_emotions": {},
            "emotional_triggers": [],
            "conversation_patterns": {},
            "growth_areas": []
        }
        
        # Count emotion frequencies
        all_emotions = []
        for entry in user_history:
            all_emotions.extend([e.name for e in entry["emotions"]])
        
        from collections import Counter
        emotion_counts = Counter(all_emotions)
        persona_insights["dominant_emotions"] = dict(emotion_counts.most_common(5))
        
        # Identify growth areas based on patterns
        recent_stability = emotion_detector._analyze_stability(update.user_id, [])[0]
        if recent_stability < 0.6:
            persona_insights["growth_areas"].append("emotional_regulation")
        
        if persona_insights["emotional_baseline"]["typical_valence"] < -0.2:
            persona_insights["growth_areas"].append("positive_coping_strategies")
        
        return {
            "user_id": update.user_id,
            "persona_insights": persona_insights,
            "recommendations": {
                "conversation_style": "supportive" if persona_insights["emotional_baseline"]["typical_valence"] < 0 else "collaborative",
                "focus_areas": persona_insights["growth_areas"],
                "emotional_support_level": "high" if recent_stability < 0.7 else "moderate"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Persona update failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "models_loaded": {
            "emotion_classifier": emotion_detector.emotion_classifier is not None,
            "sentiment_analyzer": emotion_detector.sentiment_analyzer is not None
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/user_profile/{user_id}")
async def get_user_emotional_profile(user_id: str):
    """Get comprehensive emotional profile for a user"""
    try:
        if user_id not in emotion_detector.user_emotion_history:
            return {"message": "No emotional history found for user", "user_id": user_id}
        
        history = list(emotion_detector.user_emotion_history[user_id])
        
        # Calculate comprehensive profile
        profile = {
            "user_id": user_id,
            "total_interactions": len(history),
            "emotional_patterns": {},
            "personality_indicators": {},
            "relationship_dynamics": {},
            "growth_trajectory": {},
            "recommendations": []
        }
        
        if history:
            # Emotional patterns analysis
            valences = [entry["valence"] for entry in history]
            arousals = [entry["arousal"] for entry in history]
            
            profile["emotional_patterns"] = {
                "baseline_mood": float(np.mean(valences)),
                "emotional_volatility": float(np.std(valences)),
                "energy_level": float(np.mean(arousals)),
                "emotional_range": {
                    "valence_range": [float(np.min(valences)), float(np.max(valences))],
                    "arousal_range": [float(np.min(arousals)), float(np.max(arousals))]
                }
            }
            
            # Personality indicators
            recent_entries = history[-10:] if len(history) >= 10 else history
            recent_emotions = []
            for entry in recent_entries:
                recent_emotions.extend([e.name for e in entry["emotions"]])
            
            emotion_freq = Counter(recent_emotions)
            
            profile["personality_indicators"] = {
                "emotional_expressiveness": len(set(recent_emotions)) / max(len(recent_emotions), 1),
                "predominant_emotions": dict(emotion_freq.most_common(3)),
                "emotional_complexity_avg": float(np.mean([len(entry["emotions"]) for entry in recent_entries])),
                "stability_score": emotion_detector._analyze_stability(user_id, [])[0]
            }
            
            # Growth trajectory
            if len(history) >= 5:
                early_valence = np.mean([entry["valence"] for entry in history[:5]])
                recent_valence = np.mean([entry["valence"] for entry in history[-5:]])
                
                profile["growth_trajectory"] = {
                    "mood_trend": "improving" if recent_valence > early_valence else "declining",
                    "emotional_development": recent_valence - early_valence,
                    "consistency_improvement": float(np.std(valences[-10:]) < np.std(valences[:10])) if len(history) >= 20 else 0.5
                }
            
            # Generate personalized recommendations
            if profile["emotional_patterns"]["baseline_mood"] < -0.3:
                profile["recommendations"].append("Focus on positive reinforcement and mood elevation strategies")
            
            if profile["emotional_patterns"]["emotional_volatility"] > 0.6:
                profile["recommendations"].append("Implement emotional regulation and stability techniques")
            
            if profile["personality_indicators"]["emotional_complexity_avg"] < 1.5:
                profile["recommendations"].append("Encourage emotional exploration and expression")
        
        return profile
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile generation failed: {str(e)}")

# Advanced emotion analysis utilities
class EmotionTransitionAnalyzer:
    """Analyzes emotional transitions and patterns"""
    
    @staticmethod
    def analyze_emotional_arc(emotions_sequence: List[List[DetectedEmotion]]) -> Dict:
        """Analyze the emotional arc of a conversation or session"""
        if not emotions_sequence:
            return {"arc_type": "neutral", "key_transitions": [], "emotional_climax": None}
        
        # Extract dominant emotions for each point
        dominant_emotions = []
        valence_progression = []
        
        for emotions in emotions_sequence:
            if emotions:
                dominant = emotions[0]  # Most confident emotion
                dominant_emotions.append(dominant.name)
                
                # Calculate valence for this point
                valence = emotion_detector.emotion_lexicon.get(dominant.name, {}).get("valence", 0)
                valence_progression.append(valence)
            else:
                dominant_emotions.append("neutral")
                valence_progression.append(0)
        
        # Identify arc type
        arc_type = EmotionTransitionAnalyzer._classify_emotional_arc(valence_progression)
        
        # Find key transitions
        key_transitions = EmotionTransitionAnalyzer._find_key_transitions(
            dominant_emotions, valence_progression
        )
        
        # Identify emotional climax
        climax_index = np.argmax(np.abs(valence_progression)) if valence_progression else 0
        emotional_climax = {
            "position": climax_index,
            "emotion": dominant_emotions[climax_index] if climax_index < len(dominant_emotions) else "neutral",
            "intensity": abs(valence_progression[climax_index]) if climax_index < len(valence_progression) else 0
        }
        
        return {
            "arc_type": arc_type,
            "key_transitions": key_transitions,
            "emotional_climax": emotional_climax,
            "progression": valence_progression,
            "dominant_sequence": dominant_emotions
        }
    
    @staticmethod
    def _classify_emotional_arc(valence_progression: List[float]) -> str:
        """Classify the type of emotional arc"""
        if len(valence_progression) < 3:
            return "neutral"
        
        start_avg = np.mean(valence_progression[:2])
        end_avg = np.mean(valence_progression[-2:])
        middle_avg = np.mean(valence_progression[1:-1]) if len(valence_progression) > 2 else 0
        
        # Classic story arcs
        if start_avg < middle_avg > end_avg and abs(middle_avg - start_avg) > 0.3:
            return "triumph_to_tragedy"  # Rise then fall
        elif start_avg > middle_avg < end_avg and abs(end_avg - middle_avg) > 0.3:
            return "tragedy_to_triumph"  # Fall then rise
        elif end_avg > start_avg + 0.3:
            return "progressive_improvement"
        elif end_avg < start_avg - 0.3:
            return "progressive_decline"
        elif np.std(valence_progression) > 0.5:
            return "volatile"
        else:
            return "stable"
    
    @staticmethod
    def _find_key_transitions(emotions: List[str], valences: List[float]) -> List[Dict]:
        """Find significant emotional transitions"""
        transitions = []
        
        for i in range(1, len(emotions)):
            prev_emotion = emotions[i-1]
            curr_emotion = emotions[i]
            prev_valence = valences[i-1]
            curr_valence = valences[i]
            
            # Significant transition if emotion changes and valence shift > threshold
            if prev_emotion != curr_emotion and abs(curr_valence - prev_valence) > 0.4:
                transitions.append({
                    "position": i,
                    "from_emotion": prev_emotion,
                    "to_emotion": curr_emotion,
                    "valence_shift": curr_valence - prev_valence,
                    "transition_type": "positive" if curr_valence > prev_valence else "negative"
                })
        
        return transitions

class PersonalityProfiler:
    """Advanced personality profiling based on emotional patterns"""
    
    def __init__(self):
        self.big_five_mapping = {
            # Openness to experience
            "curiosity": 0.8, "wonder": 0.7, "confusion": 0.6,
            
            # Conscientiousness  
            "guilt": 0.7, "pride": 0.8, "accomplishment": 0.9,
            
            # Extraversion
            "excitement": 0.8, "joy": 0.7, "enthusiasm": 0.9,
            
            # Agreeableness
            "empathy": 0.9, "compassion": 0.8, "gratitude": 0.7,
            
            # Neuroticism
            "anxiety": 0.8, "fear": 0.7, "worry": 0.6, "sadness": 0.5
        }
    
    def generate_personality_insights(self, emotion_history: List[Dict]) -> Dict:
        """Generate personality insights from emotional history"""
        if not emotion_history:
            return {"insufficient_data": True}
        
        # Collect all emotions with their frequencies and intensities
        emotion_patterns = defaultdict(list)
        
        for entry in emotion_history:
            for emotion in entry["emotions"]:
                emotion_patterns[emotion.name].append({
                    "intensity": emotion.intensity.value,
                    "confidence": emotion.confidence,
                    "timestamp": entry["timestamp"]
                })
        
        # Calculate Big Five approximations
        big_five = self._calculate_big_five(emotion_patterns)
        
        # Identify communication style
        communication_style = self._analyze_communication_style(emotion_history)
        
        # Determine coping mechanisms
        coping_patterns = self._identify_coping_patterns(emotion_history)
        
        # Social tendencies
        social_tendencies = self._analyze_social_patterns(emotion_patterns)
        
        return {
            "big_five_traits": big_five,
            "communication_style": communication_style,
            "coping_mechanisms": coping_patterns,
            "social_tendencies": social_tendencies,
            "confidence_level": self._calculate_profile_confidence(emotion_history)
        }
    
    def _calculate_big_five(self, emotion_patterns: Dict) -> Dict:
        """Calculate Big Five personality trait approximations"""
        # traits = {
        #     "openness": 0.5,
        #     "conscientiousness": 0.5, 
        #     "extraversion": 0.5,
        #     "agreeableness": 0.5,
        #     "neuroticism": 0.5
        # }
        traits = Big5Traits(
            # openness=0.5, 
            # conscientiousness=0.5, 
            # extraversion=0.5, 
            # agreeableness=0.5, 
            # neuroticism=0.5
        )
        
        total_weight = 0
        
        for emotion, instances in emotion_patterns.items():
            if emotion in self.big_five_mapping:
                weight: float = len(instances) * np.mean([inst["confidence"] for inst in instances])
                total_weight += weight
                
                # Map emotions to traits (simplified mapping)
                if emotion in ["curiosity", "wonder", "confusion"]:
                    # traits["openness"] += weight * 0.1
                    traits.add_openness(weight * 0.1)
                elif emotion in ["guilt", "pride"]:
                    # traits["conscientiousness"] += weight * 0.1
                    traits.add_conscientiousness(weight * 0.1)
                elif emotion in ["excitement", "joy", "enthusiasm"]:
                    # traits["extraversion"] += weight * 0.1
                    traits.add_extraversion(weight * 0.1)
                elif emotion in ["empathy", "compassion", "gratitude"]:
                    # traits["agreeableness"] += weight * 0.1
                    traits.add_agreeableness(weight * 0.1)
                elif emotion in ["anxiety", "fear", "worry", "sadness"]:
                    # traits["neuroticism"] += weight * 0.1
                    traits.add_neuroticism(weight * 0.1)
        
        # Normalize traits
        if total_weight > 0:
            for trait in traits:
                traits[trait] = min(max(traits[trait], 0.0), 1.0)
        
        return traits
    
    def _analyze_communication_style(self, emotion_history: List[Dict]) -> Dict:
        """Analyze communication style based on emotional expression"""
        if not emotion_history:
            return {}
        
        # Analyze emotional expressiveness
        avg_emotions_per_message = np.mean([len(entry["emotions"]) for entry in emotion_history])
        
        # Analyze emotional intensity
        all_intensities = []
        for entry in emotion_history:
            all_intensities.extend([e.intensity.value for e in entry["emotions"]])
        
        avg_intensity = np.mean(all_intensities) if all_intensities else 2.5
        
        # Classify communication style
        style = {
            "expressiveness": "high" if avg_emotions_per_message > 2.5 else "moderate" if avg_emotions_per_message > 1.5 else "low",
            "emotional_intensity": "high" if avg_intensity > 3.5 else "moderate" if avg_intensity > 2.5 else "low",
            "communication_pattern": "expressive" if avg_emotions_per_message > 2 and avg_intensity > 3 else "balanced" if avg_emotions_per_message > 1.5 else "reserved"
        }
        
        return style
    
    def _identify_coping_patterns(self, emotion_history: List[Dict]) -> List[str]:
        """Identify coping mechanisms based on emotional transitions"""
        patterns = []
        
        # Analyze emotional recovery patterns
        negative_to_positive_transitions = 0
        total_negative_episodes = 0
        
        for i in range(1, len(emotion_history)):
            prev_valence = emotion_history[i-1]["valence"]
            curr_valence = emotion_history[i]["valence"]
            
            if prev_valence < -0.2:
                total_negative_episodes += 1
                if curr_valence > prev_valence + 0.3:
                    negative_to_positive_transitions += 1
        
        recovery_rate = negative_to_positive_transitions / max(total_negative_episodes, 1)
        
        if recovery_rate > 0.6:
            patterns.append("resilient_recovery")
        elif recovery_rate > 0.3:
            patterns.append("moderate_coping")
        else:
            patterns.append("needs_support")
        
        # Analyze emotion regulation
        recent_volatility = np.std([entry["valence"] for entry in emotion_history[-10:]])
        if recent_volatility < 0.3:
            patterns.append("good_emotional_regulation")
        elif recent_volatility > 0.6:
            patterns.append("emotional_volatility")
        
        return patterns
    
    def _analyze_social_patterns(self, emotion_patterns: Dict) -> Dict:
        """Analyze social emotional patterns"""
        social_emotions = ["empathy", "compassion", "gratitude", "envy", "admiration"]
        social_score = 0
        
        for emotion in social_emotions:
            if emotion in emotion_patterns:
                social_score += len(emotion_patterns[emotion])
        
        return {
            "social_awareness": "high" if social_score > 10 else "moderate" if social_score > 5 else "low",
            "interpersonal_focus": social_score / max(sum(len(instances) for instances in emotion_patterns.values()), 1)
        }
    
    def _calculate_profile_confidence(self, emotion_history: List[Dict]) -> float:
        """Calculate confidence in personality profile based on data quality"""
        if len(emotion_history) < 5:
            return 0.3
        elif len(emotion_history) < 15:
            return 0.6
        elif len(emotion_history) < 30:
            return 0.8
        else:
            return 0.95

# Initialize additional analyzers
personality_profiler = PersonalityProfiler()

@app.post("/analyze_emotional_arc")
async def analyze_emotional_arc(messages: List[ChatMessage]):
    """Analyze the emotional arc of a conversation sequence"""
    try:
        emotions_sequence = []
        
        for message in messages:
            emotions = await emotion_detector.detect_emotions(message.text, message.user_id)
            emotions_sequence.append(emotions)
        
        arc_analysis = EmotionTransitionAnalyzer.analyze_emotional_arc(emotions_sequence)
        
        return {
            "emotional_arc": arc_analysis,
            "conversation_insights": {
                "total_messages": len(messages),
                "emotional_complexity": len([seq for seq in emotions_sequence if len(seq) > 1]),
                "dominant_emotional_theme": max(set(arc_analysis["dominant_sequence"]), key=arc_analysis["dominant_sequence"].count) if arc_analysis["dominant_sequence"] else "neutral"
            },
            "recommendations": {
                "conversation_management": "Consider emotional pacing" if arc_analysis["arc_type"] == "volatile" else "Maintain current flow",
                "intervention_points": [t["position"] for t in arc_analysis["key_transitions"] if t["transition_type"] == "negative"]
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Emotional arc analysis failed: {str(e)}")

@app.get("/personality_profile/{user_id}")
async def get_personality_profile(user_id: str):
    """Generate comprehensive personality profile"""
    try:
        if user_id not in emotion_detector.user_emotion_history:
            return {"message": "Insufficient data for personality profiling", "user_id": user_id}
        
        history = list(emotion_detector.user_emotion_history[user_id])
        profile = personality_profiler.generate_personality_insights(history)
        
        # Add user context
        profile["user_id"] = user_id
        profile["data_points"] = len(history)
        profile["analysis_date"] = datetime.now().isoformat()
        
        return profile
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Personality profiling failed: {str(e)}")

# WebSocket support for real-time emotion tracking
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict as TypingDict

class ConnectionManager:
    def __init__(self):
        self.active_connections: TypingDict[str, WebSocket] = {}
        
    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        
    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            
    async def send_emotion_update(self, user_id: str, emotion_data: dict):
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_json(emotion_data)
            except:
                self.disconnect(user_id)

manager = ConnectionManager()

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket endpoint for real-time emotion tracking"""
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            
            # Process emotion detection
            emotional_state = await emotion_detector.analyze_emotional_state(data, user_id)
            
            # Send real-time update
            emotion_update = {
                "timestamp": datetime.now().isoformat(),
                "emotions": [
                    {
                        "name": e.name,
                        "intensity": e.intensity.value,
                        "confidence": e.confidence
                    }
                    for e in emotional_state.dominant_emotions
                ],
                "valence": emotional_state.valence,
                "arousal": emotional_state.arousal_level,
                "stability": emotional_state.emotional_stability
            }
            
            await manager.send_emotion_update(user_id, emotion_update)
            
    except WebSocketDisconnect:
        manager.disconnect(user_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)