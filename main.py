from fastapi import FastAPI
from contextlib import asynccontextmanager
# from routes.conversations import router as convRouter
# from routes.chat import router as chatRouter
# from routes.bio_maker import router as bioRouter
from routes import bio_maker, chat, conversations
from mdb.db_manager import DatabaseManager
from ddb.ddb_manager import Dynamo_Manager
from configuration import DB_NAME, EMBEDDING_MODEL , GROQ_API_KEY, LLAMA_MODEL, MONGODB_URI
from chatbot.smart_streaming_chatbot import SmartStreamingChatbot

from chatbot.bio_bot import BioBot

import boto3
from boto3.resources.base import ServiceResource
from boto3.dynamodb.table import TableResource

import boto3

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

# # DynamoDB setup
# import boto3



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

        global chatbot
        chatbot =  SmartStreamingChatbot(mdb_manager, "")

        global biobot
        biobot = BioBot()

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