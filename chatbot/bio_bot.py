### Changing this because I don't need Graph for bio. Or do I??? Is it really needed??
### 🤔🤔🤔🤔 What if I really need to add some tools in the future.
### I mean you remember, I added some Romantic, marriage, nerd, some styles. You remember that.
### 👉👉 But still I don't think I need graph

from typing import List, AsyncGenerator, Dict, Any
from dto.requests import BioGenerationRequest
from main import mdb_manager
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import os
from langchain_groq import ChatGroq
from configuration import LLAMA_MODEL, GROQ_API_KEY
from fastapi import Depends
from llm.llm import get_llm
from responses import BioMakerResponse, BioResponse

# from bio_maker.bio_graph import create_graph
# from bio_maker.state import BioGraphState

## This is my code all
class BioBot:
    # def __init__(self, llm:ChatGroq = Depends(get_llm, )) -> None:
    def __init__(self) -> None:
        # self.workflow = self._create_flow()
        # self.llm = self._setup_llm(LLAMA_MODEL, GROQ_API_KEY)
        # self.llm = llm
        self.llm =self._setup_llm()
        pass

    # def _create_flow(self):
    #     graph = create_graph()
    #     return graph
    
    ### Because same LLM I have to setup have 2 places, One in this bot and another in chat bot. Hence, using Dependency injection - START
    ###👉 [[update]] - There will be 2 LLMs. This one will be at higher temperature for a lot creativity
    def _setup_llm(self): #, llama_model:str, grok_api_key:str):
        if LLAMA_MODEL is None or GROQ_API_KEY is None:
            raise
        if not os.environ.get("GROQ_API_KEY"):
            os.environ["GROQ_API_KEY"] = GROQ_API_KEY # grok_api_key # config["GROQ_API_KEY"]

        ## Load the LLM https://chatgpt.com/c/681f72e4-5ad0-800d-b706-dc2453ab111e
        llm = ChatGroq(
            # model=config["LLAMA_MODEL"],
            # model=llama_model,
            model = LLAMA_MODEL,
            temperature=0.7 # I need a high creativity for bio part here.
            )
        return llm
    ### ---------------------------------------- STOP

    # async def _handle_streaming_response(self, user_id: str, message: str, required_tools: List[str]) -> AsyncGenerator[Dict[str, Any], None]:
    #     """Handle complex responses with true LLM streaming"""

    #     ### Not here. But inside the graph nodes. -------------- start
    #     # # Create a comprehensive prompt
    #     # system_prompt = """You are a helpful dating app assistant. Provide thoughtful, encouraging advice.
    #     # Be conversational, supportive, and specific. If the user needs matches or profile analysis, 
    #     # acknowledge that you're working on it."""
    #     ### Not here. But inside the graph nodes. -------------- stop
    #     ### 🤔🤔 Wait, I really don't need the graph at all. Just invoke the llm.

    #     try:
    #         # yield {

    #         # }

    #         state = BioGraphState({"uid": user_id, "input": message, "profile": None, "response": None})

    #         response = await self.workflow.ainvoke(state)

    #         yield {
    #             "type": "response",
    #             "content": response,
    #             "is_final": True
    #         }

    #     except Exception as e:
    #         yield {
    #             "type": "error",
    #             "content": f"I encountered an issue: {str(e)}. Let me help you another way!",
    #             "is_final": True
    #         }

    ### -->>> This was a nice code I wrong. Unfortunately not better enough ----------- start
    # async def run_bio_maker(self, uid: str, input:str)->BioMakerResponse:
    #     profile = await db_manager.get_user_profile(uid)
    #     print(profile.model_dump_json())

    #     messages = [
    #         # 👉 For BioPrompt, I still need Claude support to nicely frame it for me. Note this time, you are not using LangGraph.
    #         # 👉👉 https://claude.ai/chat/537f692e-323c-43ad-9c43-fc5e17f416f8 Simply Wow !!!!!!!!!
    #         SystemMessage(BIO_PROMPT, profile=profile),
    #         HumanMessage(input)
    #     ]

    #     try:
    #         response = await self.llm.ainvoke(messages) ## 👉 I am not interested in streaming the bio part.
    #         ## 👉 Also adding too many options in bio part (like romantic, marriage, casual etc is too much / useless) as user can write 
    #         ## in almost infine ways now using LLM.
    #         print(response)

    #         return BioMakerResponse({"type":"response", "content": response.content.__str__()})
    #     except Exception as e:
    #         print(e)
    #         return BioMakerResponse({"type":"error", "content": "Error. Please try again!"})
    ### This was a nice code I wrong. Unfortunately not better enough ----------- stop

    ### 👉 Note, the thing is I don't know how to setup max tokens in ChatGroq one. In open api one, I know, but not here. I don't know why

    async def run_llm(self, prompt:str) -> str: ## 👉 Here we are outputting just the response content
        response = await self.llm.ainvoke(prompt)
        return response.content.__str__()

