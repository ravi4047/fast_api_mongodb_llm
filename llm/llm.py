from langchain_groq import ChatGroq
import os
from configuration import LLAMA_MODEL, GROQ_API_KEY
from transformers.pipelines import pipeline

# from langchain_community.chat_models import AzureOpenAI
from langchain_community.chat_models import AzureChatOpenAI

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
        temperature=0.3,
    )
    
    return llm

def get_llm():
    if LLAMA_MODEL is None or GROQ_API_KEY is None:
        raise ValueError("Please check or .env variables. Some variable missing...")
    return setup_llm(LLAMA_MODEL, GROQ_API_KEY)

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

# https://chatgpt.com/c/683cc494-9ad0-800d-8864-06efe6c9d592

def setup_emotion_classifier():
    # j-hartmann/emotion-english-distilroberta-base https://huggingface.co/j-hartmann/emotion-english-distilroberta-base
    # anger 🤬
    # disgust 🤢
    # fear 😨
    # joy 😀
    # neutral 😐
    # sadness 😭
    # surprise 😲
    try:
        emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)
        return emotion_classifier    
    except Exception as e:
        print(f"Error setting up emotion classifier: {e}")
        raise

def setup_emotion_sentiments():
    # SamLowe/roberta-base-go_emotions https://huggingface.co/SamLowe/roberta-base-go_emotions
    # This is a more comprehensive emotion detection model.
    try:
        emotion_sentiments = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)
        return emotion_sentiments
    except Exception as e:
        print(f"Error setting up emotion sentiments: {e}")
        raise

## Setup Phi 4 model request from azure endpoint.
# def setup_phi4_azure(): 
def setup_slm_azure():    
    # Ensure these variables are defined in configuration.py:
    # AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT_NAME
    try:
        from configuration import AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT_NAME
    except ImportError:
        raise ImportError("Please define AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, and AZURE_OPENAI_DEPLOYMENT_NAME in configuration.py")

    if not AZURE_OPENAI_ENDPOINT or not AZURE_OPENAI_API_KEY or not AZURE_OPENAI_DEPLOYMENT_NAME:
        raise ValueError("Please check your Azure OpenAI configuration variables.")

    return AzureChatOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        temperature=0.7,  # Adjust temperature as needed
        max_tokens=1000,  # Adjust max tokens as needed
        # openai_api_base=AZURE_OPENAI_ENDPOINT,
        # openai_api_key=AZURE_OPENAI_API_KEY,
        # deployment_name=AZURE_OPENAI_DEPLOYMENT_NAME
    )
