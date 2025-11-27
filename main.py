from fastapi import FastAPI
from contextlib import asynccontextmanager
# from routes.conversations import router as convRouter
# from routes.chat import router as chatRouter
# from routes.bio_maker import router as bioRouter
from llm.llm import setup_emotion_classifier, setup_emotion_sentiments, setup_slm_azure
from persona_cloning.emotion_handler import EmotionHandler
from routes import bio_maker, chat, conversations, persona

from mdb.db_manager import DatabaseManager
from ddb.ddb_manager import Dynamo_Manager
from configuration import DB_NAME, EMBEDDING_MODEL , GROQ_API_KEY, LLAMA_MODEL, MONGODB_URI
from chatbot.smart_streaming_chatbot import SmartStreamingChatbot

from chatbot.bio_bot import BioBot

import boto3
from boto3.resources.base import ServiceResource
from boto3.dynamodb.table import TableResource

import boto3

from transformers.pipelines import pipeline

# dynamodb = boto3.resource("dynamodb")
# table = dynamodb.Table("users")  # Correct way to reference an existing table

# table = boto3.resource("dynamodb").Table("users")


# from botocore.client import BaseClient

# from botocore.client import BaseClient

import logging

logger = logging.getLogger(__name__)

chatbot = None
biobot = None
mdb_manager = DatabaseManager()
ddb_manager = None

# phi4_azure = None
slm = None

# # DynamoDB setup
# import boto3

# https://chatgpt.com/c/683cc494-9ad0-800d-8864-06efe6c9d592
## Asked chatgpt to select the best one for getting quick emotions and he did this. It covers 7 emotions
# j-hartmann/emotion-english-distilroberta-base https://huggingface.co/j-hartmann/emotion-english-distilroberta-base
# anger 🤬
# disgust 🤢
# fear 😨
# joy 😀
# neutral 😐
# sadness 😭
# surprise 😲
# emotion_classifier =  pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)
# emotion_classifier = None
# emotion_sentiments = None
emotion_handler = None
### Only 7 emotions are not enough. This is an Emotion handling chatbot. So, I think I should go to GoEmotion

## `Do you know how much I love you. If you won't love me, I will kill myself. Don't you ever force me to be there. I will hate you forever if that happened`
# -> Due to this line, I was like let's focus on the emotions on a more better way.
# emotion_classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)

# sentences = ["I am not having a great day"]

# model_outputs = emotion_classifier(sentences)
# print(model_outputs)

# print(model_outputs[0])

## 

# produces a list of dicts for each of the labels

# ddd = boto3.resource("dynamodb")

# # Get the service resource.
# dynamodb = boto3.resource('dynamodb')

# # Create the DynamoDB table.
# table = dynamodb.create_table(
#     TableName='users',
#     KeySchema=[
#         {
#             'AttributeName': 'username',
#             'KeyType': 'HASH'
#         },
#         {
#             'AttributeName': 'last_name',
#             'KeyType': 'RANGE'
#         }
#     ],
#     AttributeDefinitions=[
#         {
#             'AttributeName': 'username',
#             'AttributeType': 'S'
#         },
#         {
#             'AttributeName': 'last_name',
#             'AttributeType': 'S'
#         },
#     ],
#     ProvisionedThroughput={
#         'ReadCapacityUnits': 5,
#         'WriteCapacityUnits': 5
#     }
# )

# # Wait until the table exists.
# table.wait_until_exists()

# # Print out some data about the table.
# print(table.item_count)

# from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource
# dddddd: DynamoDBServiceResource = boto3.resource("dynamodb")
# nice_table = dddddd.Table("sdfsd")
# nice_table.put_item("", )
#✅✅✅Finally done it by installing boto3-stubs[dynamodb]

@asynccontextmanager
async def lifespan(app:FastAPI):
    try:
        if DB_NAME is None or EMBEDDING_MODEL is None or MONGODB_URI is None or LLAMA_MODEL is None or GROQ_API_KEY is None:
            raise

        await mdb_manager.connect(MONGODB_URI, DB_NAME)

        
        # await ddb_manager.initialize_db()
        global ddb_manager
        ddb_manager = Dynamo_Manager()

        global emotion_classifier
        emotion_classifier = setup_emotion_classifier()

        global emotion_sentiments
        emotion_sentiments = setup_emotion_sentiments()

        global emotion_handler
        emotion_handler = EmotionHandler()

        global chatbot
        chatbot =  SmartStreamingChatbot(mdb_manager, "")

        global biobot
        biobot = BioBot()

        # global phi4_azure
        # phi4_azure = setup_phi4_azure()
        global slm
        slm = setup_slm_azure()

        logger.info("Application startup completed")
        yield
    except Exception as e:
        print(e)
    finally:
        pass

app = FastAPI(lifespan=lifespan)

app.include_router(chat.router, tags=["chat"], prefix="/chat")
app.include_router(conversations.router, tags=["conversation"], prefix="/conversation")
app.include_router(bio_maker.router, tags=["bio maker"], prefix="/bio")

# Adding the websocket persona routes
app.include_router(persona.router, tags=["persona_cloning"], prefix="/persona")