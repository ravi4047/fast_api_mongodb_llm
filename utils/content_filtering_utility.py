from typing import Tuple, List, Dict, Any
from configuration import MAX_TOXICITY_SCORE, BLOCKED_TOPICS
from openai import OpenAI
import re
import logging

logger = logging.getLogger(__name__)

client = OpenAI()

def check_explicit_content(text: str) -> Tuple[bool, float, List[str]]:
    """
    Check if text contains explicit or inappropriate content.
    
    Args:
        text: The text to check
        
    Returns:
        Tuple of (is_safe, toxicity_score, detected_topics)
    """
    # Simple pattern matching for obvious explicit content
    explicit_patterns = [
        r'\b(sex|fuck|dick|cock|pussy|vagina|tits|boobs|ass)\b',
        r'\b(anal|blowjob|handjob|cumshot|cum|jizz|horny)\b',
        r'\b(slut|whore|bitch|cunt|faggot|nigger|chink)\b'
    ]
    
    for pattern in explicit_patterns:
        if re.search(pattern, text.lower()):
            return False, 1.0, ["explicit language detected"]
    
    try:
        # Use OpenAI's moderation endpoint
        response = client.moderations.create(input=text)
        result = response.results[0]
        
        # Check if any category is flagged
        is_flagged = result.flagged
        
        # Get detected categories
        detected_topics = [
            category for category, flagged in result.categories.model_dump().items() 
            if flagged
        ]
        
        # Get highest category score as toxicity score
        scores = result.category_scores.model_dump()
        toxicity_score = max(scores.values()) if scores else 0.0
        
        return not is_flagged, toxicity_score, detected_topics
        
    except Exception as e:
        logger.error(f"Error in content moderation: {str(e)}")
        # Conservative approach - if moderation fails, we'll do a simple check
        for topic in BLOCKED_TOPICS:
            if topic.lower() in text.lower():
                return False, 1.0, [topic]
        
        return True, 0.0, []

def sanitize_message(message: str) -> str:
    """
    Sanitize a message by removing explicit content.
    This is a fallback if the message is borderline inappropriate.
    """
    # Replace common explicit terms
    explicit_terms = {
        r'\b(sex)\b': '[intimate activity]',
        r'\b(sexy|hot)\b': '[attractive]',
        r'\bfuck\b': '[explicit]',
        r'\b(boobs|tits|breasts)\b': '[body part]',
        r'\b(dick|cock|penis)\b': '[body part]',
        r'\b(pussy|vagina)\b': '[body part]',
        r'\b(ass|butt)\b': '[body part]',
    }
    
    sanitized = message
    for pattern, replacement in explicit_terms.items():
        sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)
    
    return sanitized

def is_message_appropriate(message: str) -> Tuple[bool, str]:
    """
    Check if a message is appropriate and sanitize if needed.
    
    Returns:
        Tuple of (is_appropriate, sanitized_message)
    """
    is_safe, toxicity_score, detected_topics = check_explicit_content(message)
    
    if not is_safe:
        return False, ""
    
    if toxicity_score > MAX_TOXICITY_SCORE:
        # Message is borderline inappropriate, sanitize it
        return True, sanitize_message(message)
    
    # Message is appropriate
    return True, message