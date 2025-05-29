## This is the main thing why I have become fan of this Claude
# https://claude.ai/chat/537f692e-323c-43ad-9c43-fc5e17f416f8

# Bio enhancement and post-processing
import re
from typing import List
from model.user_profile import UserProfile


class BioEnhancer:
    @staticmethod
    def enhance_bio(bio: str, user_profile: UserProfile) -> str:
        """Post-process the generated bio for final touches"""
        
        # Remove any remaining inappropriate content
        bio = re.sub(r'\b(sex|sexual|hookup|one night)\b', '', bio, flags=re.IGNORECASE)
        
        # Ensure proper capitalization
        sentences = bio.split('. ')
        enhanced_sentences = []
        
        for sentence in sentences:
            if sentence:
                sentence = sentence.strip()
                if sentence:
                    sentence = sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence.upper()
                    enhanced_sentences.append(sentence)
        
        enhanced_bio = '. '.join(enhanced_sentences)
        
        # Ensure it ends properly
        if not enhanced_bio.endswith(('.', '!', '?')):
            enhanced_bio += '.'
            
        return enhanced_bio
    
    @staticmethod
    def generate_suggestions(user_profile: UserProfile, safety_flags: List[str]) -> List[str]:
        suggestions = []
        
        if "inappropriate_content" in safety_flags:
            suggestions.append("Try focusing on your hobbies and interests instead of personal topics")
        
        if "too_short" in safety_flags:
            suggestions.append("Add more details about what you enjoy doing or what makes you unique")
        
        if "contact_information" in safety_flags:
            suggestions.append("Remove contact information - people can connect through the app")
        
        if not user_profile.interests:
            suggestions.append("Add some interests to your profile for a more personalized bio")
            
        if not user_profile.hobbies:
            suggestions.append("Include hobbies in your profile to make your bio more engaging")
        
        if len(suggestions) == 0:
            suggestions.append("Your bio looks great! Consider adding specific examples of your interests")
            
        return suggestions