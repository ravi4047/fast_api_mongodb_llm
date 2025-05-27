import re
from typing import Dict, List
from enums.intents import MessageComplexity, ResponseStrategy
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
# ==================== INTENT ANALYZER ====================

# https://claude.ai/chat/1760f327-87e7-41f0-b7b0-8ed9541afc65 
class IntentAnalyzer:
    """Analyzes user messages to determine complexity and required response strategy"""
    
    ## 👉 I am really in doubt with this. Why hardcoded?
    @staticmethod
    def analyze_message(message: str, user_profile: Dict = {}) -> tuple[MessageComplexity, ResponseStrategy, List[str]]:
        """
        Returns: (complexity, strategy, required_tools)
        """
        message_lower = message.lower()
        required_tools = []
        
        # Simple greetings and basic responses
        simple_patterns = [
            r'\b(hi|hello|hey|thanks|thank you|okay|ok|yes|no)\b',
            r'\bhow are you\b',
            r'\bwhat.*your name\b',
        ]
        
        if any(re.search(pattern, message_lower) for pattern in simple_patterns):
            return MessageComplexity.SIMPLE, ResponseStrategy.INSTANT, []
        
        # Tool-requiring patterns
        tool_patterns = {
            'get_matches': [
                r'\b(show|find|get).*matches?\b',
                r'\bwho.*available\b',
                r'\bsuggest.*someone\b',
                r'\blooking for.*date\b'
            ],
            'analyze_profile': [
                r'\banalyze.*profile\b',
                r'\btell me about.*profile\b',
                r'\bwhat.*think.*about\b'
            ],
            'relationship_advice': [
                r'\b(advice|help|tip|suggestion).*\b',
                r'\bhow.*should.*\b',
                r'\bwhat.*say\b',
                r'\bfirst date\b',
                r'\bconversation.*starter\b'
            ]
        }
        
        for tool, patterns in tool_patterns.items():
            if any(re.search(pattern, message_lower) for pattern in patterns):
                required_tools.append(tool)
        
        # Determine complexity and strategy
        if not required_tools:
            # No tools needed but might be complex question
            if len(message.split()) > 15 or '?' in message:
                return MessageComplexity.MODERATE, ResponseStrategy.FULL_STREAM, []
            else:
                return MessageComplexity.SIMPLE, ResponseStrategy.INSTANT, []
        
        elif len(required_tools) == 1:
            # Single tool usage
            if 'relationship_advice' in required_tools:
                return MessageComplexity.MODERATE, ResponseStrategy.FULL_STREAM, required_tools
            else:
                return MessageComplexity.MODERATE, ResponseStrategy.SHOW_REASONING, required_tools
        
        else:
            # Multiple tools or complex reasoning
            return MessageComplexity.COMPLEX, ResponseStrategy.SHOW_REASONING, required_tools
        

        # https://claude.ai/chat/fc84041b-e46b-4bc8-aa34-4334a48ef0b5
    # Entity Extraction Node
    # async def entity_extraction_node(state: ConversationGraphState) -> ConversationGraphState:
    #     llm = get_llm()
        
    #     # Create the entity extraction prompt
    #     system_prompt = """You are an AI assistant for a dating app. Extract important entities from the user message.
    #     Possible entity types:
    #     - user: Names of users mentioned
    #     - date: Any date or time references
    #     - location: Any location references
    #     - attribute: Profile attributes like "age", "interests", "birthday", etc.
    #     - match_status: Match-related keywords like "new matches", "unmatched", etc.
    #     - message_status: Message-related keywords like "unread", "recent", etc.
        
    #     Respond with ONLY the extracted entities in JSON format.
    #     """
        
    #     # Current user message and intent context
    #     user_message = f"User message: {state.current_message}\nDetected intent: {state.intent}"
        
    #     # Create messages
    #     messages = [
    #         SystemMessage(content=system_prompt),
    #         HumanMessage(content=f"{user_message}\nWhat entities can you extract?")
    #     ]
        
    #     # Get the entity extraction result
    #     parser = PydanticOutputParser(pydantic_object=EntityExtractionResult)
    #     try:
    #         response = await llm.ainvoke(messages)
    #         result = parser.parse(response.content)
            
    #         # Convert entities to dictionary format for easier lookup
    #         entities_dict = {}
    #         for entity in result.entities:
    #             entity_type = entity.type
    #             if entity_type not in entities_dict:
    #                 entities_dict[entity_type] = []
    #             entities_dict[entity_type].append({
    #                 "name": entity.name,
    #                 "value": entity.value
    #             })
            
    #         # Update state with extracted entities
    #         return ConversationGraphState(
    #             **state.model_dump(),
    #             entities=entities_dict
    #         )
    #     except Exception as e:
    #         return ConversationGraphState(
    #             **state.model_dump(),
    #             error=f"Entity extraction error: {str(e)}"
    #         )