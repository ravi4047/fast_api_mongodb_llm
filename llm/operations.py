from fastapi import FastAPI, Depends
# from llm.llm import get_llm, LLM_Setup
from llm.llm import get_ai_engine, AI_Engine

## LLM Operations

# def some_operation(llm_setup: LLM_Setup = Depends(get_llm)):
#     return llm_setup.llm.invoke("")

def some_operation(llm_setup: AI_Engine = Depends(get_ai_engine)):
    return llm_setup.llm.invoke("")

def some_operation2():
    return

######
# Conversation
######

