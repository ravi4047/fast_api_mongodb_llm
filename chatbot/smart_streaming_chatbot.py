## This is the 3rd and final one.
## After all Realizing that we will be doing REST + STreaming 
# https://claude.ai/chat/1760f327-87e7-41f0-b7b0-8ed9541afc65
# https://chatgpt.com/c/683566b6-5d18-800d-8c07-16cf43f7345d

# After realizing that we can halt the 
# ==================== SMART STREAMING CHATBOT ====================

from typing import Any, AsyncGenerator, Dict

from enums.intents import ResponseStrategy


class SmartStreamingChatbot:
    def __init__(self, db_manager, openai_api_key: str):
        self.db = db_manager
        openai.api_key = openai_api_key
        self.intent_analyzer = IntentAnalyzer()
        
        # Initialize tools
        self.tools = [
            GetMatchesTool(db_manager),
            RelationshipAdviceTool(db_manager)
        ]
        self.tool_executor = ToolExecutor(self.tools)
    
    async def process_message_smart(self, user_id: str, message: str) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Smart processing that chooses the right interaction pattern
        """
        # Get user context
        user_profile = await self.db.get_user_profile(user_id) if hasattr(self.db, 'get_user_profile') else {}
        
        # Analyze message complexity and strategy
        complexity, strategy, required_tools = self.intent_analyzer.analyze_message(message, user_profile)
        
        # Route to appropriate handler
        if strategy == ResponseStrategy.INSTANT:
            async for chunk in self._handle_instant_response(user_id, message):
                yield chunk
                
        elif strategy == ResponseStrategy.SHOW_REASONING:
            async for chunk in self._handle_reasoning_response(user_id, message, required_tools):
                yield chunk
                
        elif strategy == ResponseStrategy.FULL_STREAM:
            async for chunk in self._handle_streaming_response(user_id, message, required_tools):
                yield chunk
    
    async def _handle_instant_response(self, user_id: str, message: str) -> AsyncGenerator[Dict[str, Any], None]:
        """Handle simple messages with instant responses"""
        
        # Quick responses for common patterns
        quick_responses = {
            'hi': "Hi there! I'm here to help you with your dating journey. What can I do for you today?",
            'hello': "Hello! Looking for matches or need some dating advice?",
            'hey': "Hey! How can I help you find love today?",
            'thanks': "You're welcome! Let me know if you need anything else.",
            'how are you': "I'm doing great and ready to help you with dating! What's on your mind?",
        }
        
        message_lower = message.lower().strip()
        response = quick_responses.get(message_lower, 
            "I'm here to help! You can ask me to find matches, give dating advice, or answer any questions about relationships.")
        
        # Send complete response immediately
        yield {
            "type": "response",
            "content": response,
            "full_content": response,
            "is_final": True,
            "strategy": "instant",
            "metadata": {"complexity": "simple", "tools_used": []}
        }
    
    async def _handle_reasoning_response(self, user_id: str, message: str, required_tools: List[str]) -> AsyncGenerator[Dict[str, Any], None]:
        """Handle moderate complexity with step-by-step reasoning display"""
        
        # Show what we're going to do
        if required_tools:
            tools_description = ", ".join(required_tools).replace('_', ' ')
            yield {
                "type": "reasoning",
                "content": f"Let me help you with that. I'll {tools_description} to give you the best answer.",
                "step": "planning"
            }
        
        response_parts = []
        
        # Execute tools and show progress
        for tool_name in required_tools:
            yield {
                "type": "tool_usage",
                "content": f"🔍 Using {tool_name.replace('_', ' ')}...",
                "tool": tool_name,
                "status": "running"
            }
            
            # Execute tool
            if tool_name == "get_matches":
                tool_input = ToolInvocation(tool="get_matches", tool_input={"user_id": user_id})
                result = await self.tool_executor.ainvoke(tool_input)
                response_parts.append(result)
                
                yield {
                    "type": "tool_usage",
                    "content": f"✅ Found your matches!",
                    "tool": tool_name,
                    "status": "completed"
                }
                
            elif tool_name == "relationship_advice":
                advice_type = self._extract_advice_type(message)
                tool_input = ToolInvocation(
                    tool="relationship_advice", 
                    tool_input={"advice_type": advice_type, "context": message}
                )
                result = await self.tool_executor.ainvoke(tool_input)
                response_parts.append(result)
                
                yield {
                    "type": "tool_usage", 
                    "content": f"✅ Generated {advice_type} advice!",
                    "tool": tool_name,
                    "status": "completed"
                }
        
        # Combine results and provide final response
        if response_parts:
            final_response = " ".join(response_parts)
        else:
            final_response = "I'd be happy to help! Could you be more specific about what you're looking for?"
        
        yield {
            "type": "response",
            "content": final_response,
            "full_content": final_response,
            "is_final": True,
            "strategy": "reasoning",
            "metadata": {
                "complexity": "moderate",
                "tools_used": required_tools,
                "reasoning_shown": True
            }
        }
    
    async def _handle_streaming_response(self, user_id: str, message: str, required_tools: List[str]) -> AsyncGenerator[Dict[str, Any], None]:
        """Handle complex responses with true LLM streaming"""
        
        # Show initial thinking
        yield {
            "type": "thinking",
            "content": "Let me think about this carefully...",
            "step": "analyzing"
        }
        
        # Build context for LLM
        context = f"User message: {message}\n"
        if required_tools:
            context += f"I should use these tools: {', '.join(required_tools)}\n"
        
        # Create a comprehensive prompt
        system_prompt = """You are a helpful dating app assistant. Provide thoughtful, encouraging advice.
        Be conversational, supportive, and specific. If the user needs matches or profile analysis, 
        acknowledge that you're working on it."""
        
        try:
            # This is where you'd implement TRUE streaming
            # For now, simulating with OpenAI streaming
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",  # Use faster model for demo
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=300,
                temperature=0.7,
                stream=True  # TRUE streaming here
            )
            
            accumulated_response = ""
            
            # Stream real tokens as they arrive
            async for chunk in response:
                if chunk.choices[0].delta.get('content'):
                    token = chunk.choices[0].delta.content
                    accumulated_response += token
                    
                    yield {
                        "type": "response",
                        "content": token,
                        "full_content": accumulated_response,
                        "is_final": False,
                        "strategy": "stream"
                    }
            
            # Mark as final
            yield {
                "type": "response",
                "content": "",
                "full_content": accumulated_response,
                "is_final": True,
                "strategy": "stream",
                "metadata": {
                    "complexity": "complex",
                    "tools_used": required_tools,
                    "streamed": True
                }
            }
            
        except Exception as e:
            yield {
                "type": "error",
                "content": f"I encountered an issue: {str(e)}. Let me help you another way!",
                "is_final": True
            }
    
    def _extract_advice_type(self, message: str) -> str:
        """Extract advice type from message"""
        message_lower = message.lower()
        if "conversation" in message_lower or "talk" in message_lower:
            return "conversation"
        elif "date" in message_lower:
            return "first date"
        elif "profile" in message_lower:
            return "profile"
        else:
            return "general"