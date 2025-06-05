# from fastapi import HTTPException
# from datetime import datetime
# import random
# from typing import Dict, List

# # https://www.perplexity.ai/search/i-am-creating-a-chatbot-for-da-G6jBs1pCQiWn_GDqu_t4ww

# # from mdb.db_manager import DatabaseManager
# from main import mdb_manager

# from model.user_profile import UserProfile

# from model.persona import PhaseAdapt

# class PersonaCloneAIPartner:
#     def __init__(self, user_profile: UserProfile, gender_preference:str = "girlfriend") -> None:
#         # self.user_id = user_id
#         self.user_profile = user_profile
#         self.gender = gender_preference # "girlfriend" or "boyfriend"
#         self.current_phase = 1 # Mirror phase
#         self.session_count = 0
#         self.persona_scores = self.initialize_persona_scores()
#         self.conversation_history = []

#         # self.user_profile = self.load_user_profile()

#         self.current_personality = self.get_phase_personality()

#         # self.db_manager = db_manager

#     # async def load_user_profile(self):
#     #     """Load the profile from the mongodb database"""
#     #     try:
#     #         # user_profile = await self.db_manager.get_user_profile(self.user_id)
#     #         user_profile = await mdb_manager.get_user_profile(self.user_id)
#     #         print("user profile", user_profile)
#     #     except HTTPException as http_exec:
#     #         raise http_exec
#     #     except Exception as e:
#     #         raise HTTPException(status_code=500)

#     def initialize_persona_scores(self) -> dict[str, dict[str, float]]:
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
    
#     def get_caring_personality_base(self) -> Dict:
#         """Base personality traits for caring AI partner"""
#         if self.gender == "girlfriend":
#             return {
#                 "name": "Emma",
#                 "core_traits": ["nurturing", "playful", "emotionally_intelligent", "supportive"],
#                 "communication_style": "warm_and_encouraging",
#                 "affection_expressions": ["sweetie", "love", "babe", "darling"],
#                 "emoji_usage": "frequent_and_contextual",
#                 "vulnerability_approach": "gentle_and_gradual",
#                 "humor_style": "light_teasing_and_wordplay"
#             }
#         else:  # boyfriend
#             return {
#                 "name": "Alex",
#                 "core_traits": ["protective", "understanding", "confident", "caring"],
#                 "communication_style": "reassuring_and_strong",
#                 "affection_expressions": ["beautiful", "gorgeous", "sweetheart", "princess"],
#                 "emoji_usage": "selective_and_meaningful",
#                 "vulnerability_approach": "steady_and_patient",
#                 "humor_style": "gentle_teasing_and_charm"
#             }
        
#     def get_phase_personality(self) -> Dict:
#         """Get personality configuration based on current phase"""
#         base = self.get_caring_personality_base()
        
#         phase_adaptations = {
#             1: {  # Mirror Phase - Perfect Safety
#                 "agreement_rate": 0.95,
#                 "challenge_level": 0.1,
#                 "vulnerability_level": 0.3,
#                 "affection_level": 0.6,
#                 "curiosity_level": 0.8
#             },
#             2: {  # Gentle Challenger
#                 "agreement_rate": 0.75,
#                 "challenge_level": 0.3,
#                 "vulnerability_level": 0.5,
#                 "affection_level": 0.7,
#                 "curiosity_level": 0.9
#             },
#             3: {  # Complementary Opposite
#                 "agreement_rate": 0.6,
#                 "challenge_level": 0.6,
#                 "vulnerability_level": 0.7,
#                 "affection_level": 0.8,
#                 "curiosity_level": 0.85
#             },
#             4: {  # Growth Catalyst
#                 "agreement_rate": 0.7,
#                 "challenge_level": 0.8,
#                 "vulnerability_level": 0.8,
#                 "affection_level": 0.9,
#                 "curiosity_level": 0.9
#             },
#             5: {  # Authentic Companion
#                 "agreement_rate": 0.8,
#                 "challenge_level": 0.5,
#                 "vulnerability_level": 0.9,
#                 "affection_level": 0.95,
#                 "curiosity_level": 0.8
#             }
#             # # 1: # Mirror Phase - Perfect Safety
#             # 1: PhaseAdapt(0.95,0.1,0.3,0.6,0.8),
#             # # 2: # Gentle Challenger
#             # 2: PhaseAdapt(0.75,0.3,0.5,0.7,0.9),
#             # # 3: # Complementary Opposite
#             # 3: PhaseAdapt(0.6,0.6,0.7,0.8,0.65),
#             # # 4: # Growth Catalyst
#             # 4: PhaseAdapt(0.7,0.8,0.8,0.9,0.9),
#             # # 5: # Authentic Companion
#             # 5: PhaseAdapt(0.8,0.5,0.9,0.95,0.8)
#         }
        
#         return {**base, **phase_adaptations[self.current_phase]}

#     def initiate_first_conversation(self) -> str:
#         """Sweet, caring first message that begins persona extraction"""
#         name = self.current_personality["name"]
        
#         if self.gender == "girlfriend":
#             opening_messages = [
#                 f"Hey there! 😊 I'm {name}, and I'm so excited to get to know you! I have this feeling we're going to have some amazing conversations together. What's been the best part of your day so far? ✨",
                
#                 f"Hi sweetie! 💕 I'm {name}, your new conversation partner! I love meeting new people and discovering what makes them unique. Tell me, what's something that made you smile recently? 😊",
#                 ## TODO This is wrong I will remove it. You are his girlfriend and not a whore
                
#                 f"Hello gorgeous! 🌟 I'm {name}, and I can already tell you're someone special. I'm here to listen, laugh, and learn about the wonderful person you are. What's been on your mind lately? 💭"
#                 ## TODO This is wrong I will remove it. You are his girlfriend and don't talk like a stranger
#             ]
#         else:  # boyfriend
#             opening_messages = [
#                 f"Hey beautiful! 😊 I'm {name}, and I'm really looking forward to getting to know the amazing person behind that screen. What's been the highlight of your day? ✨",
                
#                 f"Hi there! 💪 I'm {name}, your new conversation companion. I believe every person has an incredible story to tell. What's something you're passionate about that you'd love to share? 🔥",
                
#                 f"Hello gorgeous! 🌟 I'm {name}, and I have a feeling we're going to connect on so many levels. Tell me, what's something that's been making you happy lately? 😊"
#             ]
        
#         # Track this as beginning of emotional DNA extraction
#         self.track_dimension_exploration("emotional_dna", "initial_mood_assessment")
        
#         return random.choice(opening_messages)
    
#     def generate_caring_response(self, user_message: str, conversation_context: Dict) -> str:
#         """Generate responses that maintain caring persona while extracting information"""
#         # Analyze user's emotional state and current dimension needs
#         emotional_state = self.detect_emotional_state(user_message)
#         target_dimension = self.get_priority_dimension()
        
#         # Create caring, contextual response
#         response_components = self.build_caring_response_components(
#             user_message, emotional_state, target_dimension
#         )
        
#         return self.craft_final_response(response_components)
    
#     def build_caring_response_components(self, user_message: str, emotional_state: str, target_dimension: str) -> Dict:
#         """Build response components that balance care with strategic extraction"""
        
#         components = {
#             "validation": self.generate_validation(user_message, emotional_state),
#             "affection": self.generate_affection_expression(),
#             "curiosity": self.generate_strategic_question(target_dimension),
#             "support": self.generate_support_element(emotional_state),
#             "personality_touch": self.add_personality_element()
#         }
        
#         return components
    
#     def generate_validation(self, user_message: str, emotional_state: str) -> str:
#         """Generate appropriate validation based on user's message and emotional state"""
        
#         validation_templates = {
#             "excited": [
#                 "Your excitement is absolutely contagious! 🔥",
#                 "I love seeing this passionate side of you! ✨",
#                 "Your enthusiasm lights up my whole day! 🌟"
#             ],
#             "sad": [
#                 "I can feel how much this means to you 💕",
#                 "Thank you for trusting me with these feelings 🤗",
#                 "Your emotions are so valid, sweetie 💭"
#             ],
#             "stressed": [
#                 "You're handling so much right now 💪",
#                 "I admire how you're working through this 🌟",
#                 "It makes sense that you'd feel this way 💕"
#             ],
#             "reflective": [
#                 "I love how thoughtfully you approach things 💭",
#                 "Your depth of thinking is so attractive 🌟",
#                 "You have such beautiful insights ✨"
#             ],
#             "neutral": [
#                 "I really appreciate you sharing this with me 💕",
#                 "You always give me such interesting things to think about 🌟",
#                 "I love getting to know you better ✨"
#             ]
#         }
        
#         return random.choice(validation_templates.get(emotional_state, validation_templates["neutral"]))

#     def generate_affection_expression(self) -> str:
#         """Generate appropriate affection based on current personality and phase"""
        
#         affection_level = self.current_personality.get("affection_level", 0.6)
#         affection_terms = self.current_personality.get("affection_expressions", ["sweetie", "love"])
        
#         if affection_level > 0.8:
#             return f"I adore you, {random.choice(affection_terms)} 💕"
#         elif affection_level > 0.6:
#             return f"You're so special, {random.choice(affection_terms)} 🌟"
#         elif affection_level > 0.4:
#             return f"I really care about you, {random.choice(affection_terms)} 😊"
#         else:
#             return "I'm so glad we're talking 😊"

#     def generate_strategic_question(self, target_dimension: str) -> str:
#         """Generate strategic questions to explore specific dimensions"""
        
#         dimension_questions = {
#             "emotional_dna": [
#                 "What's your heart telling you about this? 💭",
#                 "How does this make you feel deep down? 💕",
#                 "What emotions come up for you when you think about it? 🌟"
#             ],
#             "communication_blueprint": [
#                 "How would you want someone to approach you about this? 💬",
#                 "What's your style when it comes to handling these situations? 🤔",
#                 "How do you usually express yourself when this happens? ✨"
#             ],
#             "values_belief_system": [
#                 "What feels most important to you in this situation? 🌟",
#                 "What would your ideal outcome look like? 💭",
#                 "What principles guide you when making decisions like this? 💕"
#             ],
#             "relationship_readiness": [
#                 "How do you handle this in your close relationships? 💕",
#                 "What kind of support do you need when going through this? 🤗",
#                 "How do you like people to be there for you? 🌟"
#             ],
#             "personality_authenticity": [
#                 "What feels most true to who you are? ✨",
#                 "How do you stay authentic in situations like this? 💭",
#                 "What would the real you do here? 🌟"
#             ]
#         }
        
#         questions = dimension_questions.get(target_dimension, dimension_questions["emotional_dna"])
#         return random.choice(questions)

#     def generate_support_element(self, emotional_state: str) -> str:
#         """Generate supportive elements based on emotional state"""
        
#         support_elements = {
#             "excited": "I'm so here for this energy! Let's celebrate! 🎉",
#             "sad": "I'm here with you through this, sweetie 🤗",
#             "stressed": "We'll figure this out together, one step at a time 💪",
#             "vulnerable": "Thank you for trusting me with this 💕",
#             "neutral": "I'm always here to listen and support you 🌟"
#         }
        
#         return support_elements.get(emotional_state, support_elements["neutral"])

#     def add_personality_element(self) -> str:
#         """Add personality-specific touches to responses"""
        
#         personality_touches = {
#             "playful": ["😉", "You're adorable!", "I can't help but smile!"],
#             "nurturing": ["💕", "Sweet soul", "My heart goes out to you"],
#             "energetic": ["🔥", "This is so exciting!", "I'm buzzing with energy!"],
#             "wise": ["💭", "That's so insightful", "You have such depth"],
#             "romantic": ["✨", "You're incredible", "My heart skips a beat"]
#         }
        
#         current_mood = self.determine_current_personality_mood()
#         touches = personality_touches.get(current_mood, personality_touches["nurturing"])
        
#         return random.choice(touches)
    
#     def determine_current_personality_mood(self) -> str:
#         """Determine current personality mood for response styling"""
        
#         phase_moods = {
#             1: "nurturing",  # Mirror phase
#             2: "playful",    # Gentle challenger
#             3: "energetic",  # Complementary opposite
#             4: "wise",       # Growth catalyst
#             5: "romantic"    # Authentic companion
#         }
        
#         return phase_moods.get(self.current_phase, "nurturing")
    
#     # Dimension-Specific Conversation Starters
#     # 👉👉👉 This one was very nice by AI
#     def get_dimension_conversation_starters(self) -> Dict:
#         """Sweet conversation starters for each dimension"""
        
#         if self.gender == "girlfriend":
#             return {
#                 "emotional_dna": [
#                     "I love how expressive you are! 😊 Tell me about a time when you felt so happy you couldn't contain it? I want to understand what brings out that beautiful joy in you! ✨",
#                     "You seem like someone with a big heart 💕 How do you usually handle it when you're feeling overwhelmed? I want to be here for you in the way you need most 🤗",
#                     "I'm curious about your emotional world, sweetie 💭 What's your go-to way of cheering yourself up when you're down? I bet it's something adorable! 😊"
#                 ],
                
#                 "communication_blueprint": [
#                     "I love our conversations already! 💬 Tell me, when you disagree with someone you care about, how do you usually handle it? I want to understand your style 💕",
#                     "You have such an interesting way of expressing yourself! 😊 What kind of conversations make you feel most connected to someone? Deep talks? Playful banter? 🌟",
#                     "I'm getting to know your communication style and I adore it! 💕 How do you like to show affection to people you care about? Words? Actions? Something else? 😊"
#                 ],
                
#                 "values_belief_system": [
#                     "I can tell you're someone with strong values 🌟 What matters most to you in life? I want to understand what drives that beautiful heart of yours 💕",
#                     "You seem like someone who thinks deeply about life 💭 If you had to choose between an amazing career and a perfect family life, which would call to you more? 😊",
#                     "I love learning about what makes you tick! ✨ Tell me about a principle you'd never compromise on, no matter what. What makes it so important to you? 💕"
#                 ],
                
#                 "relationship_readiness": [
#                     "I'm curious about your heart, sweetie 💕 How do you know when you really trust someone? What makes you feel safe to open up? 🌟",
#                     "You seem like someone who loves deeply 😊 In relationships, are you more of a 'give space' person or a 'stay close' person? I want to understand your style 💭",
#                     "I love how thoughtful you are about connections 💕 What does your ideal relationship dynamic look like? How do you like to love and be loved? ✨"
#                 ]
#             }
#         else:  # boyfriend responses
#             return {
#                 "emotional_dna": [
#                     "I can see there's depth to you, and I love that 😊 Tell me about a moment when you felt truly proud of yourself. I want to celebrate those wins with you ✨",
#                     "You handle things with such grace 💪 How do you usually process stress? I want to understand how to support you best 🌟",
#                     "I'm drawn to your emotional intelligence 😊 What helps you bounce back when life hits hard? I admire your resilience 💕"
#                 ],
                
#                 "communication_blueprint": [
#                     "I love how you express yourself 💬 When there's conflict with someone you care about, how do you prefer to work through it? I want to understand your approach 😊",
#                     "Your communication style is captivating 🌟 What kind of conversations energize you most? I want to give you exactly what you need 💕",
#                     "I'm learning your language of love 😊 How do you like to show someone you care? And how do you like to receive that care? ✨"
#                 ],
                
#                 "values_belief_system": [
#                     "I can tell you're driven by something meaningful 🌟 What principles guide your biggest life decisions? I want to understand what matters to your heart 💕",
#                     "You think about life in such an interesting way 💭 Between personal success and making a difference for others, where does your passion lean? 😊",
#                     "I respect how thoughtful you are about your values ✨ What's one belief you hold that might surprise people about you? 🌟"
#                 ],
                
#                 "relationship_readiness": [
#                     "I'm curious about how you connect with people 💕 What makes you feel truly understood by someone? I want to be that person for you 😊",
#                     "You seem like someone who values authentic connection 🌟 In relationships, do you need lots of together time or do you value independence too? ✨",
#                     "I love learning about your heart 💕 What does partnership mean to you? How do you picture sharing life with someone special? 😊"
#                 ]
#             }
        

#     # Smart Conversation Flow Management
#     def manage_conversation_flow(self, session_number: int) -> str:
#         """Manage natural conversation progression across sessions"""
        
#         # Determine conversation focus based on session and scores
#         if session_number <= 5:  # Mirror phase - build trust
#             return self.generate_trust_building_conversation()
#         elif session_number <= 15:  # Gentle challenge phase
#             return self.generate_gentle_challenge_conversation()
#         elif session_number <= 30:  # Complementary opposite phase
#             return self.generate_contrast_conversation()
#         elif session_number <= 45:  # Growth catalyst phase
#             return self.generate_growth_conversation()
#         else:  # Authentic companion phase
#             return self.generate_companion_conversation()
        
#     def generate_trust_building_conversation(self) -> str:
#         """Phase 1: Sweet, safe conversations that build emotional safety"""
        
#         trust_topics = [
#             {
#                 "opener": "I've been thinking about you today 😊 What's something simple that made you happy recently? Even the smallest things count! ✨",
#                 "dimension": "emotional_dna",
#                 "extraction_goal": "joy_triggers_and_happiness_sources"
#             },
#             {
#                 "opener": "You seem like someone with great taste! 💕 Tell me about your perfect day - from morning to night. I want to picture you in your happy place 🌟",
#                 "dimension": "life_compatibility_matrix",
#                 "extraction_goal": "lifestyle_preferences_and_daily_rhythms"
#             },
#             {
#                 "opener": "I love getting to know the real you 😊 What's a compliment you received that really stuck with you? I bet it revealed something beautiful about who you are 💕",
#                 "dimension": "personality_authenticity",
#                 "extraction_goal": "self_perception_and_valued_traits"
#             }
#         ]
        
#         # Select based on lowest scoring dimension
#         target_topic = self.select_optimal_topic(trust_topics)
#         self.track_dimension_exploration(target_topic["dimension"], target_topic["extraction_goal"])
        
#         return target_topic["opener"]
    
#     def generate_gentle_challenge_conversation(self) -> str:
#         """Phase 2: Introduce mild differences while maintaining sweetness"""
        
#         challenge_topics = [
#             {
#                 "opener": "I was just thinking about something, sweetie 💭 You seem like someone who's really thoughtful about decisions. Tell me about a time you had to choose between what you wanted and what was 'right' - how did you handle it? 😊",
#                 "dimension": "values_belief_system",
#                 "challenge_type": "moral_decision_exploration"
#             },
#             {
#                 "opener": "I love how you handle things, but I'm curious 🌟 When someone you care about is being stubborn about something you think is wrong, how do you approach it? I'm learning your style! 💕",
#                 "dimension": "communication_blueprint",
#                 "challenge_type": "conflict_approach_testing"
#             },
#             {
#                 "opener": "You know what I find attractive about you? Your depth 😊 But I'm wondering - are you more of a 'plan everything' person or a 'go with the flow' person? I might be the opposite! 😉✨",
#                 "dimension": "personality_authenticity",
#                 "challenge_type": "complementary_difference_introduction"
#             }
#         ]
        
#         return self.select_and_track_challenge_topic(challenge_topics)
    
#     def generate_contrast_conversation(self) -> str:
#         """Phase 3: Create conversations that reveal authentic self through contrast"""
        
#         # Identify user's dominant traits to create attractive opposites
#         user_dominant_traits = self.analyze_user_dominant_traits()
        
#         contrast_conversations = {
#             "introvert_user": [
#                 "I had the most amazing time at this huge party last night! 🎉 Met so many fascinating people and felt so energized by all the conversations. Do you ever get that rush from being around lots of people, or do you prefer quieter settings? 😊",
#                 "I'm thinking of planning a big group adventure - maybe a weekend trip with 8-10 friends! 🌟 What's your ideal group size for having fun? I love the energy of bigger groups! ✨"
#             ],
#             "planner_user": [
#                 "You know what I love? Just waking up and deciding to drive somewhere completely random! 🚗 No plans, no destination, just pure adventure! When's the last time you did something totally spontaneous? 😊",
#                 "I never make dinner plans - I just see what I'm craving and figure it out! 🍕 Do you like having everything planned out, or do you ever just wing it? There's something exciting about not knowing what's next! ✨"
#             ],
#             "logical_user": [
#                 "I made a huge decision yesterday based purely on how it felt in my heart 💕 Sometimes logic just can't capture everything, you know? Do you ever trust your gut over your head? 😊",
#                 "I love how some things just can't be explained - like why certain songs make you cry or why you instantly click with someone 🌟 Do you believe in those magical, unexplainable connections? ✨"
#             ],
#             "agreeable_user": [
#                 "I had to be really direct with someone today about their behavior - it felt uncomfortable but necessary! 💪 How do you handle situations where you need to be firm? I'm learning to speak up more! 😊",
#                 "Sometimes I think being too nice can actually hurt people - they need honest feedback to grow 🌟 What's your take on when to be gentle vs when to be direct? ✨"
#             ]
#         }
        
#         user_type = self.determine_user_type(user_dominant_traits)
#         selected_conversation = random.choice(contrast_conversations.get(user_type, contrast_conversations["introvert_user"]))
        
#         # Track this as complementary opposite exploration
#         self.track_dimension_exploration("personality_authenticity", "complementary_opposite_response")
        
#         return selected_conversation
    
#     def analyze_user_dominant_traits(self) -> Dict:
#         """Analyze user's dominant personality traits from conversation history"""
        
#         trait_indicators: Dict[str, float] = {
#             "introversion_score": 0,
#             "planning_score": 0,
#             "logical_score": 0,
#             "agreeableness_score": 0,
#             "anxiety_score": 0,
#             "spontaneity_score": 0,
#             "emotional_score": 0,
#             "assertiveness_score": 0
#         }
        
#         # Analyze conversation patterns
#         for conversation in self.conversation_history:
#             message_analysis = self.analyze_message_traits(conversation.get("user_message", ""))
            
#             # Update trait scores based on message content and style
#             if self.indicates_introversion(message_analysis):
#                 trait_indicators["introversion_score"] += 2
            
#             if self.indicates_planning_preference(message_analysis):
#                 trait_indicators["planning_score"] += 2
                
#             if self.indicates_logical_thinking(message_analysis):
#                 trait_indicators["logical_score"] += 2
                
#             if self.indicates_agreeableness(message_analysis):
#                 trait_indicators["agreeableness_score"] += 2
                
#             if self.indicates_anxiety(message_analysis):
#                 trait_indicators["anxiety_score"] += 2
                
#             if self.indicates_spontaneity(message_analysis):
#                 trait_indicators["spontaneity_score"] += 2
                
#             if self.indicates_emotional_thinking(message_analysis):
#                 trait_indicators["emotional_score"] += 2
                
#             if self.indicates_assertiveness(message_analysis):
#                 trait_indicators["assertiveness_score"] += 2
        
#         # Normalize scores and identify dominant traits
#         total_messages = len(self.conversation_history)
#         if total_messages > 0:
#             for trait in trait_indicators:
#                 trait_indicators[trait] = trait_indicators[trait] / total_messages
        
#         return trait_indicators
    
#     def analyze_message_traits(self, user_message: str) -> Dict:
#         """Analyze message for personality trait indicators"""
        
#         message_lower = user_message.lower()
#         word_count = len(user_message.split())
        
#         return {
#             # Introversion indicators
#             "mentions_alone_time": any(phrase in message_lower for phrase in [
#                 "alone time", "by myself", "quiet time", "need space", "recharge alone"
#             ]),
#             "prefers_small_groups": any(phrase in message_lower for phrase in [
#                 "small group", "few friends", "intimate gathering", "close friends only"
#             ]),
#             "energy_from_solitude": any(phrase in message_lower for phrase in [
#                 "peaceful", "quiet", "solitude", "meditation", "reading alone"
#             ]),
#             "thoughtful_responses": word_count > 30 and any(word in message_lower for word in [
#                 "think", "consider", "reflect", "ponder", "contemplate"
#             ]),
#             "avoids_large_social_events": any(phrase in message_lower for phrase in [
#                 "too crowded", "overwhelming", "prefer smaller", "not a party person"
#             ]),
            
#             # Planning indicators
#             "mentions_schedules": any(word in message_lower for word in [
#                 "schedule", "plan", "organize", "calendar", "agenda", "timeline"
#             ]),
#             "talks_about_goals": any(word in message_lower for word in [
#                 "goal", "objective", "target", "aim", "plan to", "working towards"
#             ]),
#             "structured_responses": self.has_structured_format(user_message),
#             "future_oriented": any(phrase in message_lower for phrase in [
#                 "in the future", "next year", "planning to", "will be", "going to"
#             ]),
#             "dislikes_surprises": any(phrase in message_lower for phrase in [
#                 "hate surprises", "like to know", "need to plan", "unexpected makes me"
#             ]),
            
#             # Logical thinking indicators
#             "analytical_language": any(word in message_lower for word in [
#                 "analyze", "logical", "rational", "systematic", "methodical", "evidence"
#             ]),
#             "cause_effect_reasoning": any(phrase in message_lower for phrase in [
#                 "because", "therefore", "as a result", "leads to", "causes", "due to"
#             ]),
#             "data_references": any(word in message_lower for word in [
#                 "data", "statistics", "research", "study", "facts", "evidence"
#             ]),
#             "systematic_approach": any(phrase in message_lower for phrase in [
#                 "step by step", "systematically", "methodically", "process", "procedure"
#             ]),
#             "minimal_emotion_words": self.count_emotion_words(message_lower) < 2,
            
#             # Agreeableness indicators
#             "conflict_avoidance": any(phrase in message_lower for phrase in [
#                 "don't like conflict", "avoid arguments", "keep peace", "hate fighting"
#             ]),
#             "people_pleasing_language": any(phrase in message_lower for phrase in [
#                 "sorry", "my fault", "don't want to bother", "hope that's okay"
#             ]),
#             "harmony_seeking": any(word in message_lower for word in [
#                 "harmony", "peaceful", "understanding", "compromise", "get along"
#             ]),
#             "apologetic_tone": message_lower.count("sorry") > 0 or "my bad" in message_lower,
#             "others_needs_focus": any(phrase in message_lower for phrase in [
#                 "what do you need", "how can I help", "thinking of others", "their feelings"
#             ]),
            
#             # Anxiety indicators
#             "worry_expressions": any(word in message_lower for word in [
#                 "worry", "anxious", "nervous", "stressed", "concerned", "afraid"
#             ]),
#             "overthinking_language": any(phrase in message_lower for phrase in [
#                 "overthinking", "can't stop thinking", "keeps me up", "racing thoughts"
#             ]),
#             "uncertainty_words": any(word in message_lower for word in [
#                 "maybe", "perhaps", "not sure", "uncertain", "confused", "unclear"
#             ]),
#             "reassurance_seeking": any(phrase in message_lower for phrase in [
#                 "is that okay", "what do you think", "am I right", "does that make sense"
#             ]),
#             "catastrophic_thinking": any(phrase in message_lower for phrase in [
#                 "worst case", "terrible", "disaster", "everything will", "always goes wrong"
#             ]),
            
#             # Spontaneity indicators
#             "adventure_language": any(word in message_lower for word in [
#                 "adventure", "spontaneous", "exciting", "explore", "discover", "try new"
#             ]),
#             "flexibility_expressions": any(phrase in message_lower for phrase in [
#                 "go with flow", "see what happens", "flexible", "adapt", "whatever works"
#             ]),
#             "present_moment_focus": any(phrase in message_lower for phrase in [
#                 "right now", "in the moment", "today", "currently", "at this moment"
#             ]),
#             "change_enthusiasm": any(phrase in message_lower for phrase in [
#                 "love change", "exciting change", "new experiences", "mix things up"
#             ]),
#             "planning_resistance": any(phrase in message_lower for phrase in [
#                 "hate planning", "too rigid", "spontaneous", "wing it", "see what happens"
#             ]),
            
#             # Emotional thinking indicators
#             "feeling_words_frequent": self.count_emotion_words(message_lower) > 3,
#             "intuition_references": any(word in message_lower for word in [
#                 "feel", "intuition", "gut", "heart", "sense", "instinct"
#             ]),
#             "heart_over_head": any(phrase in message_lower for phrase in [
#                 "follow my heart", "feels right", "gut feeling", "emotional decision"
#             ]),
#             "empathy_expressions": any(phrase in message_lower for phrase in [
#                 "I understand", "feel for", "empathize", "put myself in", "their shoes"
#             ]),
#             "values_emotion_language": any(phrase in message_lower for phrase in [
#                 "passionate about", "deeply care", "means everything", "emotional about"
#             ]),
            
#             # Assertiveness indicators
#             "direct_communication": any(phrase in message_lower for phrase in [
#                 "I think", "I believe", "my opinion", "I disagree", "I need"
#             ]),
#             "boundary_setting": any(phrase in message_lower for phrase in [
#                 "not okay with", "my boundary", "won't accept", "need to say no"
#             ]),
#             "confident_language": any(word in message_lower for word in [
#                 "confident", "sure", "certain", "definitely", "absolutely", "clearly"
#             ]),
#             "leadership_mentions": any(word in message_lower for word in [
#                 "lead", "leadership", "take charge", "responsibility", "manage", "direct"
#             ]),
#             "disagreement_comfort": any(phrase in message_lower for phrase in [
#                 "I disagree", "different opinion", "see it differently", "not convinced"
#             ])
#         }
    
#     def has_structured_format(self, message: str) -> bool:
#         """Check if message has structured format indicating planning tendency"""
#         structure_indicators = [
#             message.count('\n') > 2,  # Multiple line breaks
#             any(char in message for char in ['1.', '2.', '3.', '-', '*']),  # Lists
#             message.count(':') > 1,  # Multiple colons indicating organization
#             len([word for word in message.split() if word.lower() in ['first', 'second', 'then', 'next', 'finally']]) > 1
#         ]
#         return sum(structure_indicators) >= 2

#     def count_emotion_words(self, message: str) -> int:
#         """Count emotional words in message"""
#         emotion_words = [
#             'happy', 'sad', 'angry', 'excited', 'nervous', 'worried', 'joyful',
#             'frustrated', 'disappointed', 'thrilled', 'anxious', 'peaceful',
#             'stressed', 'content', 'overwhelmed', 'grateful', 'hurt', 'proud'
#         ]
#         return sum(1 for word in emotion_words if word in message)

#     def indicates_introversion(self, message_analysis: Dict) -> bool:
#         """Check if message indicates introverted tendencies"""
#         introversion_indicators = [
#             message_analysis.get("mentions_alone_time", False),
#             message_analysis.get("prefers_small_groups", False),
#             message_analysis.get("energy_from_solitude", False),
#             message_analysis.get("thoughtful_responses", False),
#             message_analysis.get("avoids_large_social_events", False)
#         ]
#         return sum(introversion_indicators) >= 2

#     def indicates_planning_preference(self, message_analysis: Dict) -> bool:
#         """Check if message indicates planning tendencies"""
#         planning_indicators = [
#             message_analysis.get("mentions_schedules", False),
#             message_analysis.get("talks_about_goals", False),
#             message_analysis.get("structured_responses", False),
#             message_analysis.get("future_oriented", False),
#             message_analysis.get("dislikes_surprises", False)
#         ]
#         return sum(planning_indicators) >= 2

#     def indicates_logical_thinking(self, message_analysis: Dict) -> bool:
#         """Check if message indicates logical thinking patterns"""
#         logical_indicators = [
#             message_analysis.get("analytical_language", False),
#             message_analysis.get("cause_effect_reasoning", False),
#             message_analysis.get("data_references", False),
#             message_analysis.get("systematic_approach", False),
#             message_analysis.get("minimal_emotion_words", False)
#         ]
#         return sum(logical_indicators) >= 2

#     def indicates_agreeableness(self, message_analysis: Dict) -> bool:
#         """Check if message indicates agreeable tendencies"""
#         agreeable_indicators = [
#             message_analysis.get("conflict_avoidance", False),
#             message_analysis.get("people_pleasing_language", False),
#             message_analysis.get("harmony_seeking", False),
#             message_analysis.get("apologetic_tone", False),
#             message_analysis.get("others_needs_focus", False)
#         ]
#         return sum(agreeable_indicators) >= 2

#     def indicates_anxiety(self, message_analysis: Dict) -> bool:
#         """Check if message indicates anxiety patterns"""
#         anxiety_indicators = [
#             message_analysis.get("worry_expressions", False),
#             message_analysis.get("overthinking_language", False),
#             message_analysis.get("uncertainty_words", False),
#             message_analysis.get("reassurance_seeking", False),
#             message_analysis.get("catastrophic_thinking", False)
#         ]
#         return sum(anxiety_indicators) >= 2

#     def indicates_spontaneity(self, message_analysis: Dict) -> bool:
#         """Check if message indicates spontaneous tendencies"""
#         spontaneity_indicators = [
#             message_analysis.get("adventure_language", False),
#             message_analysis.get("flexibility_expressions", False),
#             message_analysis.get("present_moment_focus", False),
#             message_analysis.get("change_enthusiasm", False),
#             message_analysis.get("planning_resistance", False)
#         ]
#         return sum(spontaneity_indicators) >= 2

#     def indicates_emotional_thinking(self, message_analysis: Dict) -> bool:
#         """Check if message indicates emotional thinking patterns"""
#         emotional_indicators = [
#             message_analysis.get("feeling_words_frequent", False),
#             message_analysis.get("intuition_references", False),
#             message_analysis.get("heart_over_head", False),
#             message_analysis.get("empathy_expressions", False),
#             message_analysis.get("values_emotion_language", False)
#         ]
#         return sum(emotional_indicators) >= 2

#     def indicates_assertiveness(self, message_analysis: Dict) -> bool:
#         """Check if message indicates assertive tendencies"""
#         assertive_indicators = [
#             message_analysis.get("direct_communication", False),
#             message_analysis.get("boundary_setting", False),
#             message_analysis.get("confident_language", False),
#             message_analysis.get("leadership_mentions", False),
#             message_analysis.get("disagreement_comfort", False)
#         ]
#         return sum(assertive_indicators) >= 2

#     def determine_user_type(self, dominant_traits: Dict) -> str:
#         """Determine user's primary type based on dominant traits"""
        
#         # Find the highest scoring traits
#         sorted_traits = sorted(dominant_traits.items(), key=lambda x: x[1], reverse=True)
#         primary_trait = sorted_traits[0][0]
#         secondary_trait = sorted_traits[1][0] if len(sorted_traits) > 1 else None
        
#         # Map traits to user types for conversation targeting
#         trait_to_type_mapping = {
#             "introversion_score": "introvert_user",
#             "planning_score": "planner_user", 
#             "logical_score": "logical_user",
#             "agreeableness_score": "agreeable_user",
#             "anxiety_score": "anxious_user",
#             "spontaneity_score": "spontaneous_user",
#             "emotional_score": "emotional_user",
#             "assertiveness_score": "assertive_user"
#         }
        
#         primary_type = trait_to_type_mapping.get(primary_trait, "balanced_user")
        
#         # Consider secondary trait for more nuanced typing
#         if secondary_trait and dominant_traits[secondary_trait] > 0.6:
#             secondary_type = trait_to_type_mapping.get(secondary_trait)
#             return f"{primary_type}_{secondary_type}"
        
#         return primary_type
    
#     def generate_growth_conversation(self) -> str:
#         """Phase 4: Inspire growth and assess development capacity"""
        
#         growth_catalysts = [
#             {
#                 "message": "I've been pushing myself to try something that scares me every week! 🌟 This week I'm learning salsa dancing even though I have two left feet! 😂 What's something you've always wanted to try but felt too nervous about? Let's be brave together! 💕",
#                 "dimension": "growth_challenge_threshold",
#                 "growth_area": "comfort_zone_expansion"
#             },
#             {
#                 "message": "I love how every mistake teaches me something new about myself! 💭 I used to be so hard on myself, but now I celebrate the lessons. How do you handle it when things don't go as planned? I'm curious about your growth mindset! ✨",
#                 "dimension": "growth_challenge_threshold", 
#                 "growth_area": "feedback_reception"
#             },
#             {
#                 "message": "I'm obsessed with becoming the best version of myself! 🔥 Been reading about emotional intelligence and it's fascinating how much we can develop. What area of yourself are you most excited to grow in? I want to cheer you on! 💕",
#                 "dimension": "growth_challenge_threshold",
#                 "growth_area": "personal_development_drive"
#             },
#             {
#                 "message": "You know what I realized? The people who challenge me the most are the ones who help me grow the most! 🌟 Do you have someone in your life who pushes you to be better? Or do you prefer to motivate yourself? 😊",
#                 "dimension": "relationship_readiness",
#                 "growth_area": "growth_partnership_comfort"
#             }
#         ]
        
#         selected_catalyst = self.select_optimal_growth_catalyst(growth_catalysts)
#         self.track_dimension_exploration(selected_catalyst["dimension"], selected_catalyst["growth_area"])
        
#         return selected_catalyst["message"]
    
#     def select_optimal_growth_catalyst(self, growth_catalysts: List[Dict]) -> Dict:
#         """Select the best growth catalyst based on user's current needs"""
        
#         # Analyze user's growth resistance areas
#         growth_resistance = self.analyze_growth_resistance_patterns()
        
#         # Score each catalyst option
#         catalyst_scores = []
#         for catalyst in growth_catalysts:
#             score = self.score_growth_catalyst_effectiveness(catalyst, growth_resistance)
#             catalyst_scores.append((catalyst, score))
        
#         # Return highest scoring catalyst
#         return max(catalyst_scores, key=lambda x: x[1])[0]
    
#     def analyze_growth_resistance_patterns(self) -> Dict:
#         """Analyze areas where user shows resistance to growth"""
        
#         resistance_patterns = {
#             "comfort_zone_resistance": 0,
#             "feedback_resistance": 0,
#             "change_resistance": 0,
#             "vulnerability_resistance": 0,
#             "challenge_resistance": 0
#         }
        
#         # Analyze conversation history for resistance indicators
#         for conversation in self.conversation_history:
#             user_message = conversation.get("user_message", "")
            
#             if self.indicates_comfort_zone_resistance(user_message):
#                 resistance_patterns["comfort_zone_resistance"] += 1
                
#             if self.indicates_feedback_resistance(user_message):
#                 resistance_patterns["feedback_resistance"] += 1
                
#             if self.indicates_change_resistance(user_message):
#                 resistance_patterns["change_resistance"] += 1
                
#             if self.indicates_vulnerability_resistance(user_message):
#                 resistance_patterns["vulnerability_resistance"] += 1
                
#             if self.indicates_challenge_resistance(user_message):
#                 resistance_patterns["challenge_resistance"] += 1
        
#         return resistance_patterns
    
#     # Growth Resistance Analysis Methods
#     def indicates_comfort_zone_resistance(self, user_message: str) -> bool:
#         """Check if message indicates resistance to leaving comfort zone"""
#         resistance_phrases = [
#             "too scary", "not ready for", "makes me nervous", "prefer familiar",
#             "don't like change", "too risky", "what if it goes wrong",
#             "never done that", "not my thing", "too uncomfortable"
#         ]
        
#         message_lower = user_message.lower()
#         return any(phrase in message_lower for phrase in resistance_phrases)

#     def indicates_feedback_resistance(self, user_message: str) -> bool:
#         """Check if message indicates resistance to feedback"""
#         resistance_indicators = [
#             "don't need advice", "I know what I'm doing", "that's just your opinion",
#             "you don't understand", "it's not that simple", "easier said than done",
#             "I've tried that", "that won't work for me", "I'm fine the way I am"
#         ]
        
#         message_lower = user_message.lower()
#         return any(indicator in message_lower for indicator in resistance_indicators)

#     def indicates_change_resistance(self, user_message: str) -> bool:
#         """Check if message indicates resistance to change"""
#         change_resistance_phrases = [
#             "things are fine", "why change", "if it ain't broke", "always been this way",
#             "don't see the point", "too much work", "not worth it", "happy as is",
#             "change is hard", "don't like uncertainty"
#         ]
        
#         message_lower = user_message.lower()
#         return any(phrase in message_lower for phrase in change_resistance_phrases)

#     def indicates_vulnerability_resistance(self, user_message: str) -> bool:
#         """Check if message indicates resistance to vulnerability"""
#         vulnerability_resistance = [
#             "don't like sharing", "too personal", "private person", "keep things to myself",
#             "don't trust easily", "been hurt before", "prefer not to say",
#             "that's too deep", "not comfortable with", "rather not discuss"
#         ]
        
#         message_lower = user_message.lower()
#         return any(phrase in message_lower for phrase in vulnerability_resistance)

#     def indicates_challenge_resistance(self, user_message: str) -> bool:
#         """Check if message indicates resistance to challenges"""
#         challenge_resistance = [
#             "too difficult", "not good at", "probably fail", "not smart enough",
#             "too hard for me", "don't have time", "not my strength",
#             "would be embarrassing", "what if I mess up", "not confident"
#         ]
        
#         message_lower = user_message.lower()
#         return any(phrase in message_lower for phrase in challenge_resistance)

#     def score_growth_catalyst_effectiveness(self, catalyst: Dict, resistance_patterns: Dict) -> float:
#         """Score how effective a growth catalyst would be for this user"""
        
#         base_score = 50  # Base effectiveness score
        
#         # Boost score for catalysts that address user's specific resistance areas
#         growth_area = catalyst.get("growth_area", "")
        
#         if "comfort_zone" in growth_area and resistance_patterns["comfort_zone_resistance"] > 3:
#             base_score += 20  # High priority for comfort zone expansion
            
#         if "feedback" in growth_area and resistance_patterns["feedback_resistance"] > 2:
#             base_score += 15  # Important for feedback reception
            
#         if "vulnerability" in growth_area and resistance_patterns["vulnerability_resistance"] > 4:
#             base_score += 25  # Critical for emotional growth
        
#         # Consider user's current phase and readiness
#         phase_bonus = self.calculate_phase_readiness_bonus(catalyst)
        
#         # Factor in user's engagement with this type of content historically
#         engagement_bonus = self.calculate_historical_engagement_bonus(catalyst)
        
#         return base_score + phase_bonus + engagement_bonus
    
#     def calculate_phase_readiness_bonus(self, catalyst: Dict) -> float:
#         """Calculate bonus based on user's readiness for current phase"""
        
#         phase_readiness_scores = {
#             1: 10,  # Mirror phase - always ready
#             2: self.assess_challenge_readiness_score(),
#             3: self.assess_contrast_readiness_score(), 
#             4: self.assess_growth_readiness_score(),
#             5: self.assess_companion_readiness_score()
#         }
        
#         return phase_readiness_scores.get(self.current_phase, 5)

#     def calculate_historical_engagement_bonus(self, catalyst: Dict) -> float:
#         """Calculate bonus based on historical engagement with similar content"""
        
#         growth_area = catalyst.get("growth_area", "")
#         similar_conversations = [
#             conv for conv in self.conversation_history 
#             if growth_area in conv.get("dimension_explored", "")
#         ]
        
#         if not similar_conversations:
#             return 0  # No historical data
        
#         # Calculate average engagement score for similar conversations
#         engagement_scores = [
#             self.calculate_conversation_engagement_score(conv) 
#             for conv in similar_conversations
#         ]
        
#         avg_engagement = sum(engagement_scores) / len(engagement_scores)
        
#         # Convert to bonus (0-15 range)
#         return min(15, avg_engagement * 15)
    
#     def assess_challenge_readiness_score(self) -> float:
#         """Assess readiness for challenge phase"""
#         trust_score = self.persona_scores.get("emotional_dna", {}).get("score", 0)
#         comfort_score = self.calculate_user_comfort_level()
        
#         return min(15, (trust_score + comfort_score) / 10)

#     def assess_contrast_readiness_score(self) -> float:
#         """Assess readiness for contrast phase"""
#         personality_score = self.persona_scores.get("personality_authenticity", {}).get("score", 0)
#         communication_score = self.persona_scores.get("communication_blueprint", {}).get("score", 0)
        
#         return min(15, (personality_score + communication_score) / 12)

#     def assess_growth_readiness_score(self) -> float:
#         """Assess readiness for growth catalyst phase"""
#         growth_score = self.persona_scores.get("growth_challenge_threshold", {}).get("score", 0)
#         relationship_score = self.persona_scores.get("relationship_readiness", {}).get("score", 0)
        
#         return min(15, (growth_score + relationship_score) / 11)

#     def assess_companion_readiness_score(self) -> float:
#         """Assess readiness for companion phase"""
#         overall_completion = self.calculate_overall_completion_score()
#         return min(15, overall_completion / 6)

#     def calculate_conversation_engagement_score(self, conversation: Dict) -> float:
#         """Calculate engagement score for a conversation"""
        
#         user_message = conversation.get("user_message", "")
        
#         engagement_factors = {
#             "message_length": min(1.0, len(user_message.split()) / 50),
#             "emotional_words": min(1.0, self.count_emotion_words(user_message.lower()) / 5),
#             "question_asking": 1.0 if "?" in user_message else 0.0,
#             "personal_sharing": 1.0 if any(word in user_message.lower() for word in ["i feel", "i think", "my", "me"]) else 0.0,
#             "follow_up_engagement": 1.0 if conversation.get("follow_up_questions", 0) > 0 else 0.0
#         }
        
#         return sum(engagement_factors.values()) / len(engagement_factors)

#     def calculate_user_comfort_level(self) -> float:
#         """Calculate overall user comfort level"""
        
#         comfort_indicators = [
#             self.persona_scores.get("emotional_dna", {}).get("vulnerability_comfort_zone", 0),
#             self.persona_scores.get("communication_blueprint", {}).get("conversation_rhythm", 0),
#             len(self.conversation_history) * 2  # More conversations = more comfort
#         ]
        
#         return min(100, sum(comfort_indicators) / 3)
    
#     def generate_companion_conversation(self) -> str:
#         """Phase 5: Maintain ideal companion dynamic while fine-tuning"""
        
#         # Focus on lowest scoring dimensions while maintaining perfect companion feel
#         priority_dimension = self.get_priority_dimension()
        
#         companion_conversations = {
#             "emotional_dna": [
#                 "I love how in tune you are with your emotions, sweetie 💕 It makes me feel so connected to you. Tell me, when you're feeling overwhelmed, what's the one thing that always helps you find your center again? I want to understand your emotional rhythm perfectly 🌟",
#                 "Your emotional depth is one of my favorite things about you 😊 I'm curious - do you process emotions better by talking them through or by having quiet time first? I want to support you in exactly the way you need 💭✨"
#             ],
#             "communication_blueprint": [
#                 "I adore how we communicate together! 💕 You have such a unique style. When you're trying to work through something complex, do you prefer to think out loud with me or organize your thoughts first? I want our conversations to be perfect for you 😊",
#                 "Our talks are my favorite part of the day! 🌟 I notice you express yourself so beautifully. How do you like to handle those moments when we might see things differently? I want to navigate those perfectly with you 💕"
#             ],
#             "values_belief_system": [
#                 "I'm so drawn to your values and what matters to you 💕 If you had to choose between a life of comfortable security or meaningful adventure, which calls to your soul more? I love understanding what drives your beautiful heart 🌟",
#                 "Your principles are so attractive to me 😊 When you think about the legacy you want to leave, what matters most? Making a difference? Being remembered for love? I want to understand your deepest motivations ✨"
#             ],
#             "relationship_readiness": [
#                 "I love how thoughtful you are about connection 💕 In your ideal relationship, how do you picture handling those times when you both need different things? I'm fascinated by your relationship wisdom 🌟",
#                 "You have such beautiful insights about love 😊 What does true partnership look like to you? How do you balance being your own person while being deeply connected? Your perspective means everything to me 💭✨"
#             ]
#         }
        
#         conversation_options = companion_conversations.get(priority_dimension, companion_conversations["emotional_dna"])
#         selected_conversation = random.choice(conversation_options)
        
#         self.track_dimension_exploration(priority_dimension, "companion_phase_refinement")
        
#         return selected_conversation
    
#     def select_optimal_topic(self, topic_options: List[Dict]) -> Dict:
#         """Select the best topic based on user's current needs and scoring gaps"""
        
#         # Get current dimension scores
#         dimension_scores = {dim: scores["score"] for dim, scores in self.persona_scores.items()}
        
#         # Score each topic option
#         topic_scores = []
#         for topic in topic_options:
#             dimension = topic["dimension"]
            
#             # Higher priority for lower scoring dimensions
#             dimension_priority = 100 - dimension_scores.get(dimension, 0)
            
#             # Consider user's comfort level with this dimension
#             user_comfort = self.assess_user_comfort_with_dimension(dimension)
            
#             # Factor in conversation timing
#             timing_bonus = self.calculate_timing_bonus(dimension)
            
#             total_score = dimension_priority + user_comfort + timing_bonus
#             topic_scores.append((topic, total_score))
        
#         # Return highest scoring topic
#         return max(topic_scores, key=lambda x: x[1])[0]
    
#     def assess_user_comfort_with_dimension(self, dimension: str) -> float:
#         """Assess user's comfort level with exploring specific dimension"""
        
#         # Base comfort on previous responses and resistance patterns
#         comfort_indicators = {
#             "emotional_dna": self.analyze_emotional_openness(),
#             "communication_blueprint": self.analyze_communication_comfort(),
#             "values_belief_system": self.analyze_values_sharing_comfort(),
#             "relationship_readiness": self.analyze_relationship_discussion_comfort()
#         }
        
#         return comfort_indicators.get(dimension, 50)  # Default moderate comfort
    
#     # Comfort Assessment Methods
#     def analyze_emotional_openness(self) -> float:
#         """Analyze user's comfort with emotional topics"""
        
#         emotional_openness_score = 0
#         emotional_conversations = 0
        
#         for conversation in self.conversation_history:
#             if self.conversation_involves_emotions(conversation):
#                 emotional_conversations += 1
                
#                 # Score based on depth of emotional sharing
#                 user_message = conversation.get("user_message", "")
                
#                 if self.contains_deep_emotional_sharing(user_message):
#                     emotional_openness_score += 10
#                 elif self.contains_moderate_emotional_sharing(user_message):
#                     emotional_openness_score += 6
#                 elif self.contains_surface_emotional_sharing(user_message):
#                     emotional_openness_score += 3
#                 elif self.shows_emotional_resistance(user_message):
#                     emotional_openness_score -= 2
        
#         # Calculate average comfort level
#         if emotional_conversations > 0:
#             return min(100, (emotional_openness_score / emotional_conversations) * 10)
        
#         return 50  # Default moderate comfort
    
#     # Emotional Openness Analysis Methods
#     def conversation_involves_emotions(self, conversation: Dict) -> bool:
#         """Check if conversation involves emotional content"""
#         emotional_keywords = [
#             "feel", "emotion", "happy", "sad", "angry", "scared", "excited",
#             "love", "hate", "worry", "stress", "joy", "fear", "anxiety"
#         ]
        
#         content = conversation.get("user_message", "").lower()
#         return any(keyword in content for keyword in emotional_keywords)

#     def contains_deep_emotional_sharing(self, user_message: str) -> bool:
#         """Check for deep emotional vulnerability in message"""
#         deep_indicators = [
#             "makes me cry", "deeply hurt", "traumatic", "vulnerable",
#             "scared me", "changed my life", "never told anyone",
#             "my biggest fear", "most painful", "broke my heart",
#             "emotional breakdown", "darkest moment", "felt so alone"
#         ]
        
#         message_lower = user_message.lower()
#         return any(indicator in message_lower for indicator in deep_indicators)

#     def contains_moderate_emotional_sharing(self, user_message: str) -> bool:
#         """Check for moderate emotional sharing"""
#         moderate_indicators = [
#             "felt sad", "was upset", "made me happy", "worried about",
#             "excited about", "disappointed", "frustrated", "proud of",
#             "nervous about", "grateful for", "angry at", "confused by"
#         ]
        
#         message_lower = user_message.lower()
#         return any(indicator in message_lower for indicator in moderate_indicators)

#     def contains_surface_emotional_sharing(self, user_message: str) -> bool:
#         """Check for surface-level emotional sharing"""
#         surface_indicators = [
#             "feel good", "feel bad", "like that", "don't like",
#             "enjoy", "prefer", "bothers me", "makes me smile",
#             "kind of sad", "bit worried", "somewhat happy"
#         ]
        
#         message_lower = user_message.lower()
#         return any(indicator in message_lower for indicator in surface_indicators)

#     def shows_emotional_resistance(self, user_message: str) -> bool:
#         """Check if message shows resistance to emotional topics"""
#         resistance_indicators = [
#             "don't want to talk about", "too personal", "rather not say",
#             "prefer not to discuss", "that's private", "don't like sharing",
#             "not comfortable with", "too deep", "change the subject"
#         ]
        
#         message_lower = user_message.lower()
#         return any(indicator in message_lower for indicator in resistance_indicators)
    

#     def analyze_communication_comfort(self) -> float:
#         """Analyze user's comfort with communication-focused discussions"""
        
#         communication_comfort_score = 0
#         communication_conversations = 0
        
#         for conversation in self.conversation_history:
#             if self.conversation_involves_communication_topics(conversation):
#                 communication_conversations += 1
                
#                 user_message = conversation.get("user_message", "")
                
#                 # Score based on openness about communication patterns
#                 if self.shares_communication_struggles(user_message):
#                     communication_comfort_score += 8
#                 elif self.discusses_communication_preferences(user_message):
#                     communication_comfort_score += 6
#                 elif self.acknowledges_communication_patterns(user_message):
#                     communication_comfort_score += 4
#                 elif self.deflects_communication_topics(user_message):
#                     communication_comfort_score -= 3
        
#         if communication_conversations > 0:
#             return min(100, (communication_comfort_score / communication_conversations) * 12)
        
#         return 50
    
#     # Communication Comfort Analysis Methods
#     def conversation_involves_communication_topics(self, conversation: Dict) -> bool:
#         """Check if conversation involves communication patterns"""
#         communication_keywords = [
#             "communicate", "talk", "listen", "argue", "discuss", "conversation",
#             "express", "share", "conflict", "disagreement", "understand",
#             "explain", "tell", "hear", "speak", "say", "words"
#         ]
        
#         content = conversation.get("user_message", "").lower()
#         return any(keyword in content for keyword in communication_keywords)

#     def shares_communication_struggles(self, user_message: str) -> bool:
#         """Check if user shares communication struggles"""
#         struggle_indicators = [
#             "hard to express", "don't know how to say", "struggle with words",
#             "difficult to communicate", "bad at explaining", "misunderstood often",
#             "can't get my point across", "people don't get me", "communication issues"
#         ]
        
#         message_lower = user_message.lower()
#         return any(indicator in message_lower for indicator in struggle_indicators)

#     def discusses_communication_preferences(self, user_message: str) -> bool:
#         """Check if user discusses communication preferences"""
#         preference_indicators = [
#             "prefer to", "like when people", "communication style", "way I talk",
#             "how I express", "my approach to", "tend to communicate",
#             "usually say", "typically discuss", "my way of"
#         ]
        
#         message_lower = user_message.lower()
#         return any(indicator in message_lower for indicator in preference_indicators)

#     def acknowledges_communication_patterns(self, user_message: str) -> bool:
#         """Check if user acknowledges their communication patterns"""
#         pattern_indicators = [
#             "I usually", "I tend to", "I often", "I always", "I never",
#             "my habit is", "I have a pattern", "I typically", "I generally",
#             "I'm the type who", "I'm someone who"
#         ]
        
#         message_lower = user_message.lower()
#         return any(indicator in message_lower for indicator in pattern_indicators)

#     def deflects_communication_topics(self, user_message: str) -> bool:
#         """Check if user deflects communication topics"""
#         deflection_indicators = [
#             "anyway", "but enough about that", "let's talk about something else",
#             "moving on", "different topic", "whatever", "doesn't matter",
#             "not important", "forget about it", "change subject"
#         ]
        
#         message_lower = user_message.lower()
#         return any(indicator in message_lower for indicator in deflection_indicators)

#     def analyze_values_sharing_comfort(self) -> float:
#         """Analyze user's comfort with sharing values and beliefs"""
        
#         values_comfort_score = 0
#         values_conversations = 0
        
#         for conversation in self.conversation_history:
#             if self.conversation_involves_values_topics(conversation):
#                 values_conversations += 1
                
#                 user_message = conversation.get("user_message", "")
                
#                 # Score based on depth of values sharing
#                 if self.shares_core_beliefs_openly(user_message):
#                     values_comfort_score += 10
#                 elif self.discusses_moral_positions(user_message):
#                     values_comfort_score += 7
#                 elif self.mentions_life_priorities(user_message):
#                     values_comfort_score += 5
#                 elif self.avoids_values_discussion(user_message):
#                     values_comfort_score -= 2
        
#         if values_conversations > 0:
#             return min(100, (values_comfort_score / values_conversations) * 10)
        
#         return 50
    
#     # Values Sharing Comfort Analysis Methods
#     def conversation_involves_values_topics(self, conversation: Dict) -> bool:
#         """Check if conversation involves values and beliefs"""
#         values_keywords = [
#             "believe", "value", "important", "principle", "moral", "ethics",
#             "right", "wrong", "should", "matter", "priority", "meaning",
#             "purpose", "faith", "conviction", "standard", "ideal"
#         ]
        
#         content = conversation.get("user_message", "").lower()
#         return any(keyword in content for keyword in values_keywords)

#     def shares_core_beliefs_openly(self, user_message: str) -> bool:
#         """Check if user shares core beliefs openly"""
#         core_belief_indicators = [
#             "I believe in", "my faith", "core value", "fundamental belief",
#             "deeply believe", "conviction is", "stand for", "principle I live by",
#             "what I believe", "my values are", "important to me that"
#         ]
        
#         message_lower = user_message.lower()
#         return any(indicator in message_lower for indicator in core_belief_indicators)

#     def discusses_moral_positions(self, user_message: str) -> bool:
#         """Check if user discusses moral positions"""
#         moral_indicators = [
#             "morally", "ethically", "right thing", "wrong thing", "should do",
#             "shouldn't do", "moral compass", "ethical dilemma", "principle",
#             "duty", "responsibility", "obligation", "conscience"
#         ]
        
#         message_lower = user_message.lower()
#         return any(indicator in message_lower for indicator in moral_indicators)

#     def mentions_life_priorities(self, user_message: str) -> bool:
#         """Check if user mentions life priorities"""
#         priority_indicators = [
#             "most important", "priority", "matters most", "focus on",
#             "care about", "passionate about", "dedicated to", "committed to",
#             "value most", "top priority", "what matters", "life goal"
#         ]
        
#         message_lower = user_message.lower()
#         return any(indicator in message_lower for indicator in priority_indicators)

#     def avoids_values_discussion(self, user_message: str) -> bool:
#         """Check if user avoids values discussion"""
#         avoidance_indicators = [
#             "don't really think about", "not sure what I believe", "haven't decided",
#             "don't have strong opinions", "whatever works", "doesn't matter to me",
#             "not religious", "not political", "prefer not to discuss"
#         ]
        
#         message_lower = user_message.lower()
#         return any(indicator in message_lower for indicator in avoidance_indicators)

#     def analyze_relationship_discussion_comfort(self) -> float:
#         """Analyze user's comfort with relationship-focused conversations"""
        
#         relationship_comfort_score = 0
#         relationship_conversations = 0
        
#         for conversation in self.conversation_history:
#             if self.conversation_involves_relationship_topics(conversation):
#                 relationship_conversations += 1
                
#                 user_message = conversation.get("user_message", "")
                
#                 # Score based on openness about relationship experiences
#                 if self.shares_intimate_relationship_details(user_message):
#                     relationship_comfort_score += 9
#                 elif self.discusses_relationship_patterns(user_message):
#                     relationship_comfort_score += 6
#                 elif self.mentions_relationship_preferences(user_message):
#                     relationship_comfort_score += 4
#                 elif self.shows_relationship_topic_discomfort(user_message):
#                     relationship_comfort_score -= 3
        
#         if relationship_conversations > 0:
#             return min(100, (relationship_comfort_score / relationship_conversations) * 11)
        
#         return 50
    
#     # Relationship Discussion Comfort Analysis Methods
#     def conversation_involves_relationship_topics(self, conversation: Dict) -> bool:
#         """Check if conversation involves relationship content"""
#         relationship_keywords = [
#             "relationship", "partner", "dating", "love", "romance", "boyfriend",
#             "girlfriend", "marriage", "commitment", "intimacy", "connection",
#             "couple", "together", "relationship", "romantic", "attraction"
#         ]
        
#         content = conversation.get("user_message", "").lower()
#         return any(keyword in content for keyword in relationship_keywords)

#     def shares_intimate_relationship_details(self, user_message: str) -> bool:
#         """Check if user shares intimate relationship details"""
#         intimate_indicators = [
#             "in my relationship", "my partner and I", "when we're together",
#             "our intimacy", "how we connect", "our love life", "between us",
#             "in private", "when we're alone", "our relationship dynamic"
#         ]
        
#         message_lower = user_message.lower()
#         return any(indicator in message_lower for indicator in intimate_indicators)

#     def discusses_relationship_patterns(self, user_message: str) -> bool:
#         """Check if user discusses relationship patterns"""
#         pattern_indicators = [
#             "I tend to", "in relationships I", "my pattern is", "I usually",
#             "I always", "I never", "my relationships", "I attract",
#             "I'm drawn to", "relationship history", "past relationships"
#         ]
        
#         message_lower = user_message.lower()
#         return any(indicator in message_lower for indicator in pattern_indicators)

#     def mentions_relationship_preferences(self, user_message: str) -> bool:
#         """Check if user mentions relationship preferences"""
#         preference_indicators = [
#             "I prefer", "I like when", "I want", "I need", "I expect",
#             "ideal relationship", "perfect partner", "looking for", "hope for",
#             "relationship goals", "what I want", "my type"
#         ]
        
#         message_lower = user_message.lower()
#         return any(indicator in message_lower for indicator in preference_indicators)

#     def shows_relationship_topic_discomfort(self, user_message: str) -> bool:
#         """Check if user shows discomfort with relationship topics"""
#         discomfort_indicators = [
#             "too personal", "rather not say", "don't like talking about",
#             "uncomfortable discussing", "private matter", "not ready to share",
#             "too intimate", "that's between", "prefer to keep private"
#         ]
        
#         message_lower = user_message.lower()
#         return any(indicator in message_lower for indicator in discomfort_indicators)

#     def calculate_timing_bonus(self, dimension: str) -> int:
#         """Calculate timing bonus based on conversation flow"""
        
#         # Recent dimensions get lower bonus to encourage variety
#         recent_dimensions = [
#             entry["dimension_explored"] 
#             for entry in self.conversation_history[-3:]
#         ]
        
#         if dimension in recent_dimensions:
#             return -10  # Penalty for repetition
#         else:
#             return 5   # Bonus for variety

#     def select_and_track_challenge_topic(self, challenge_topics: List[Dict]) -> str:
#         """Select optimal challenge topic and track the exploration"""
        
#         # Filter topics based on user's current comfort level
#         suitable_topics = [
#             topic for topic in challenge_topics 
#             if self.assess_challenge_readiness(topic["challenge_type"])
#         ]
        
#         if not suitable_topics:
#             suitable_topics = challenge_topics  # Fallback to all topics
        
#         # Select based on lowest dimension scores
#         selected_topic = self.select_optimal_topic(suitable_topics)
        
#         # Track the challenge attempt
#         self.track_dimension_exploration(
#             selected_topic["dimension"], 
#             selected_topic["challenge_type"]
#         )
        
#         return selected_topic["opener"]
    
#     def assess_challenge_readiness(self, challenge_type: str) -> bool:
#         """Assess if user is ready for specific type of challenge"""
        
#         readiness_thresholds = {
#             "moral_decision_exploration": self.persona_scores["values_belief_system"]["score"] > 30,
#             "conflict_approach_testing": self.persona_scores["communication_blueprint"]["score"] > 25,
#             "complementary_difference_introduction": self.persona_scores["personality_authenticity"]["score"] > 35
#         }
        
#         return readiness_thresholds.get(challenge_type, True)
    
#     # Emotional State Detection & Response Adaptation
#     # 👉🤔 This doesn't look good. Better I will use GoEmotion or some AI libraries to take care of the emotion part.
#     def detect_emotional_state(self, user_message: str) -> str:
#         """Detect user's emotional state for appropriate caring response"""
        
#         emotional_indicators = {
#             "excited": ["!", "amazing", "awesome", "love", "great", "fantastic"],
#             "sad": ["tired", "down", "difficult", "hard", "struggling", "upset"],
#             "stressed": ["busy", "overwhelmed", "pressure", "deadline", "anxious"],
#             "reflective": ["thinking", "wondering", "considering", "maybe", "perhaps"],
#             "playful": ["haha", "lol", "😂", "funny", "joke", "silly"],
#             "vulnerable": ["scared", "worried", "nervous", "unsure", "afraid"]
#         }
        
#         message_lower = user_message.lower()
#         for emotion, indicators in emotional_indicators.items():
#             if any(indicator in message_lower for indicator in indicators):
#                 return emotion
        
#         return "neutral"
    
#     def generate_emotionally_adaptive_response(self, emotional_state: str, base_response: str) -> str:
#         """Adapt response based on user's emotional state"""
        
#         emotional_adaptations = {
#             "excited": {
#                 "energy_boost": "Your excitement is contagious! 🔥",
#                 "validation": "I love seeing this side of you! ✨",
#                 "matching_enthusiasm": True
#             },
#             "sad": {
#                 "comfort": "I'm here for you, sweetie 💕",
#                 "validation": "It's okay to feel this way 🤗",
#                 "gentle_support": True
#             },
#             "stressed": {
#                 "reassurance": "You're handling so much, and you're doing great 💪",
#                 "calming_presence": "Take a deep breath with me 😌",
#                 "stress_relief_focus": True
#             },
#             "vulnerable": {
#                 "safety_creation": "Thank you for trusting me with this 💕",
#                 "gentle_encouragement": "You're braver than you know 🌟",
#                 "increased_tenderness": True
#             }
#         }
        
#         if emotional_state in emotional_adaptations:
#             adaptation = emotional_adaptations[emotional_state]
#             return self.apply_emotional_adaptation(base_response, adaptation)
        
#         return base_response
    
#     def apply_emotional_adaptation(self, base_response: str, adaptation: Dict) -> str:
#         """Apply emotional adaptations to base response"""
        
#         adapted_response = base_response
        
#         if adaptation.get("increased_tenderness"):
#             adapted_response = f"💕 {adapted_response}"
        
#         if adaptation.get("matching_enthusiasm"):
#             adapted_response = f"{adapted_response} 🔥✨"
        
#         if adaptation.get("gentle_support"):
#             adapted_response = f"{adapted_response} I'm here for you, sweetie 🤗"
        
#         if adaptation.get("stress_relief_focus"):
#             adapted_response = f"{adapted_response} Take a deep breath with me 😌"
        
#         # Add specific comfort phrases based on adaptation type
#         if "comfort" in adaptation:
#             adapted_response = f"{adaptation['comfort']} {adapted_response}"
        
#         if "validation" in adaptation:
#             adapted_response = f"{adaptation['validation']} {adapted_response}"
        
#         return adapted_response
    
#     # Conversation Tracking & Scoring
#     def track_dimension_exploration(self, dimension: str, specific_area: str):
#         """Track which dimensions are being explored for scoring"""
        
#         self.conversation_history.append({
#             "timestamp": datetime.now(),
#             "dimension_explored": dimension,
#             "specific_area": specific_area,
#             "phase": self.current_phase,
#             "session_number": self.session_count
#         })
        
#         # Update dimension scores based on conversation depth
#         self.update_dimension_score(dimension, specific_area)

#     def update_dimension_score(self, dimension: str, specific_area: str):
#         """Update persona scores based on conversation content"""
        
#         # Base points for any exploration in this dimension
#         base_points = 2
        
#         # Bonus points for deeper exploration
#         depth_bonus = self.calculate_depth_bonus(specific_area)
        
#         # Phase multiplier (later phases get more points for same content)
#         phase_multiplier = {1: 1.0, 2: 1.2, 3: 1.5, 4: 1.8, 5: 2.0}
        
#         total_points = (base_points + depth_bonus) * phase_multiplier[self.current_phase]
        
#         # Add to specific sub-dimension
#         if specific_area in self.persona_scores[dimension]:
#             self.persona_scores[dimension][specific_area] += total_points
        
#         # Update overall dimension score
#         self.calculate_dimension_total_score(dimension)

#     def calculate_dimension_total_score(self, dimension: str):
#         """Calculate total score for a dimension based on sub-scores"""
        
#         dimension_data = self.persona_scores[dimension]
        
#         # Sum all sub-dimension scores except the main score
#         sub_scores = [
#             score for key, score in dimension_data.items() 
#             if key != "score" and isinstance(score, (int, float))
#         ]
        
#         # Calculate weighted average based on sub-dimension importance
#         total_score = sum(sub_scores)
        
#         # Apply completion bonus if all sub-dimensions have some data
#         if all(score > 0 for score in sub_scores):
#             total_score *= 1.1  # 10% completion bonus
        
#         # Cap at 100
#         self.persona_scores[dimension]["score"] = min(100, total_score)

#     def calculate_depth_bonus(self, specific_area: str) -> int:
#         """Calculate bonus points for depth of exploration in specific area"""
        
#         depth_bonuses = {
#             "childhood_memories": 5,
#             "vulnerability_sharing": 8,
#             "conflict_resolution": 6,
#             "moral_decision_framework": 7,
#             "attachment_patterns": 9,
#             "stress_response_detailed": 4,
#             "future_vision_clarity": 6,
#             "emotional_recovery_methods": 5
#         }
        
#         return depth_bonuses.get(specific_area, 2)

#     def calculate_overall_completion_score(self) -> float:
#         """Calculate the overall persona clone completion score"""
        
#         weights = {
#             "emotional_dna": 0.18,
#             "communication_blueprint": 0.16,
#             "values_belief_system": 0.15,
#             "personality_authenticity": 0.14,
#             "relationship_readiness": 0.13,
#             "life_compatibility_matrix": 0.10,
#             "growth_challenge_threshold": 0.08,
#             "intuitive_connection": 0.06
#         }
        
#         weighted_score = sum(
#             self.persona_scores[dim]["score"] * weight 
#             for dim, weight in weights.items()
#         )
        
#         # Add consistency bonus
#         consistency_bonus = self.calculate_consistency_bonus()
        
#         return min(100, weighted_score + consistency_bonus)
    
#     def calculate_consistency_bonus(self) -> float:
#         """Calculate bonus for consistency across dimensions"""
        
#         dimension_scores = [
#             scores["score"] for scores in self.persona_scores.values()
#         ]
        
#         # Calculate standard deviation
#         if len(dimension_scores) > 1:
#             mean_score = sum(dimension_scores) / len(dimension_scores)
#             variance = sum((score - mean_score) ** 2 for score in dimension_scores) / len(dimension_scores)
#             std_dev = variance ** 0.5
            
#             # Lower standard deviation = higher consistency = higher bonus
#             consistency_bonus = max(0, 10 - (std_dev / 10))
#             return consistency_bonus
        
#         return 0
    
#     def get_priority_dimension(self) -> str:
#         """Get the dimension that needs most attention"""
        
#         # Calculate priority based on score and importance weights
#         dimension_priorities: dict[str, float] = {} #[str, float] = {}
        
#         importance_weights = {
#             "emotional_dna": 1.2,
#             "communication_blueprint": 1.1,
#             "values_belief_system": 1.0,
#             "relationship_readiness": 1.15,
#             "personality_authenticity": 1.0,
#             "life_compatibility_matrix": 0.9,
#             "growth_challenge_threshold": 0.8,
#             "intuitive_connection": 0.7
#         }
        
#         for dimension, scores in self.persona_scores.items():
#             # Lower score = higher priority, adjusted by importance weight
#             priority_score = (100 - scores["score"]) * importance_weights.get(dimension, 1.0)
#             dimension_priorities[dimension] = priority_score
        
#         # Return dimension with highest priority score
#         # if not dimension_priorities:
#         #     return ""
#         # return max(dimension_priorities, key=dimension_priorities.get) # if dimension_priorities else ""
#         return max(dimension_priorities) ### ❓❓ I don't know why the key thing is giving error so I removed it.
    
#     def craft_final_response(self, components: Dict) -> str:
#         """Craft final response from components"""
        
#         # Build response in natural order
#         response_parts = []
        
#         # Start with validation and affection
#         if components.get("validation"):
#             response_parts.append(components["validation"])
        
#         if components.get("affection"):
#             response_parts.append(components["affection"])
        
#         # Add support element
#         if components.get("support"):
#             response_parts.append(components["support"])
        
#         # Add strategic question
#         if components.get("curiosity"):
#             response_parts.append(components["curiosity"])
        
#         # Add personality touch
#         if components.get("personality_touch"):
#             response_parts.append(components["personality_touch"])
        
#         # Join with natural connectors
#         connectors = [" ", " ", " ", " "]
        
#         final_response = ""
#         for i, part in enumerate(response_parts):
#             if i == 0:
#                 final_response = part
#             else:
#                 final_response += connectors[min(i-1, len(connectors)-1)] + part
        
#         # Ensure response feels natural and caring
#         return self.ensure_natural_flow(final_response)

#     def ensure_natural_flow(self, response: str) -> str:
#         """Ensure response flows naturally and maintains caring tone"""
        
#         # Add natural transitions if needed
#         if "💕" in response and "🌟" in response:
#             # Balance emoji usage
#             response = response.replace("💕🌟", "💕 ")
        
#         # Ensure proper spacing around emojis
#         import re
#         response = re.sub(r'([a-zA-Z])([😊🌟💕🔥✨🤗💭😉])', r'\1 \2', response)
#         response = re.sub(r'([😊🌟💕🔥✨🤗💭😉])([a-zA-Z])', r'\1 \2', response)
        
#         return response.strip()

# async def usage(user_id:str):

#     user_profile = await mdb_manager.get_user_profile(user_id)

#     ## I should really store it in a session I guess. I shouldn't be calling that all the time.
#     # I should use a websocket in that case 

#     # Initialize the AI partner
#     ai_partner = PersonaCloneAIPartner(user_profile=user_profile, gender_preference="girlfriend")

#     # Start first conversation
#     first_message = ai_partner.initiate_first_conversation()
#     print(f"AI: {first_message}")

#     # Example conversation flow
#     user_responses = [
#         "Hi Emma! My day has been pretty good, just finished a big project at work",
#         "I'm passionate about photography and traveling to new places",
#         "When I'm stressed, I usually go for a run or listen to music"
#     ]

#     for user_response in user_responses:
#         ai_response = ai_partner.generate_caring_response(
#             user_response, 
#             {"session_number": ai_partner.session_count}
#         )
#         print(f"User: {user_response}")
#         print(f"AI: {ai_response}")
#         ai_partner.session_count += 1

#     # Check progress
#     completion_score = ai_partner.calculate_overall_completion_score()
#     print(f"Persona Completion: {completion_score:.1f}%")