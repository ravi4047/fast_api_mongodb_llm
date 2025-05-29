# Safety and content filtering
import re
from typing import List


class ContentFilter:
    INAPPROPRIATE_PATTERNS = [
        r'\b(sex|sexual|hook\s*up|one\s*night|nudes?|naked)\b',
        r'\b(drugs?|weed|cocaine|marijuana|high|stoned)\b',
        r'\b(hate|racist?|homophobic|transphobic)\b',
        r'\b(violence|violent|fight|kill|murder)\b',
        r'\b(money|rich|wealth|gold\s*digger|sugar)\b',
        r'\b(desperate|lonely|depressed|suicidal)\b'
    ]
    
    CONTACT_INFO_PATTERNS = [
        r'\b\d{10,}\b',  # Phone numbers
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
        r'\b(?:instagram|insta|snap|snapchat|whatsapp|telegram)\b',  # Social media
    ]
    
    @classmethod
    def check_content_safety(cls, text: str) -> List[str]:
        flags = []
        text_lower = text.lower()
        
        for pattern in cls.INAPPROPRIATE_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                flags.append("inappropriate_content")
                break
        
        for pattern in cls.CONTACT_INFO_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                flags.append("contact_information")
                break
        
        if len(text.strip()) < 10:
            flags.append("too_short")
        
        if text.count('!') > 5 or text.count('?') > 3:
            flags.append("excessive_punctuation")
            
        return flags