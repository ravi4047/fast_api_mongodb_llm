from enum import Enum
# ==================== RESPONSE STRATEGY ENUM ====================

class ResponseStrategy(str, Enum):
    INSTANT = "instant"          # Simple responses, no tools needed
    SHOW_REASONING = "reasoning" # Show what I'm doing step by step
    FULL_STREAM = "stream"       # Full streaming for complex LLM responses

class MessageComplexity(str, Enum):
    SIMPLE = "simple"       # Greetings, simple questions
    MODERATE = "moderate"   # Single tool usage, basic reasoning
    COMPLEX = "complex"     # Multiple tools, deep reasoning, long responses