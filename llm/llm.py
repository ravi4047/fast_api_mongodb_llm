from langchain_groq import ChatGroq
import os
from mongodb_statefulqa_bot_pythondb.configuration import GROQ_API_KEY
from configuration import LLAMA_MODEL

# from  config_py import config

# class AI_Engine():
#     def __init__(self) -> None:        

def setup_llm(llama_model:str, grok_api_key:str):
    if not os.environ.get("GROQ_API_KEY"):
        os.environ["GROQ_API_KEY"] = grok_api_key # config["GROQ_API_KEY"]

    ## Load the LLM https://chatgpt.com/c/681f72e4-5ad0-800d-b706-dc2453ab111e
    llm = ChatGroq(
        # model=config["LLAMA_MODEL"],
        model=llama_model,
          temperature=0.3)
    return llm

### ------------------ WE ARE NOT DOING THIS. WE ARE JUST MAKING IN DEPENDENCY INJECTION -------- START
# class AiEngine:
#     # llm: ChatGroq = None

#     def __init__(self) -> None:
#         if self.llm is None:
#             self.llm = setup_llm("", "")
#         # return llm

# # Create a singleton instance
# ai_engine = AiEngine()
### ------------------ WE ARE NOT DOING THIS. WE ARE JUST MAKING IN DEPENDENCY INJECTION -------- STOP

## 🤔🤔 I have used this but I am still not convinced. I will talk about this in chatbots and try to convince myself taking fast api lifespan 
## in matter.
## Let's ask Claude.

### ----------------- ------------------ ----------------- ---------- 

# class LLM_Setup:
class AI_Engine:
    def __init__(self) -> None:
        if self.llm is None:
            if not os.environ.get("GROQ_API_KEY") and GROQ_API_KEY is not None:
                os.environ["GROQ_API_KEY"] = GROQ_API_KEY # config["GROQ_API_KEY"]
            # self.llm = setup_llm("sdfdsf", "sdddddd")
            self.llm = ChatGroq(
                # model=config["LLAMA_MODEL"],
                model=LLAMA_MODEL or "",
                temperature=0.3)
            
            self.conversational_llm = ChatGroq(
                # model=config["LLAMA_MODEL"],
                model=LLAMA_MODEL or "",
                temperature=0.7)

## This one is for Dependency Injection https://chatgpt.com/c/681f72e4-5ad0-800d-b706-dc2453ab111e
def get_ai_engine():
    return AI_Engine()