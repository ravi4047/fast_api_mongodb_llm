from fastapi import FastAPI, Depends
from pymongo import MongoClient, AsyncMongoClient
from pymongo.database import Database

from typing import Annotated

from dotenv import dotenv_values

from configuration import PROFILES_COLLECTION, MATCHES_COLLECTION, MESSAGES_COLLECTION, FEEDS_HISTORY_COLLECTION, CHAT_HISTORY_COLLECTION

config = dotenv_values(".env")

# def setup_mongodb_old(app: FastAPI):
#     # Load the mongodb database ================================== ================================== start
    # db_client = MongoClient(config["MONGODB_ATLAS_URI"])
    # app.mongodb_client = db_client # MongoClient(config["MONGODB_ATLAS_URI"])
    # app.database = app.mongodb_client[config["MONGODB_DB_NAME"]]
    # print("Connected to the MongoDB database!", )

    # print(app.database.list_collections().to_list())    
    # Load the mongodb database ================================== ================================== stop

def setup_mongodb2(mongodb_uri:str, db_name:str):
    # Load the mongodb database ================================== ================================== start
    db_client = MongoClient(mongodb_uri)
    
    # app.mongodb_client = db_client # MongoClient(config["MONGODB_ATLAS_URI"])
    # app.database = app.mongodb_client[config["MONGODB_DB_NAME"]]
    print("Connected to the MongoDB database!", )

    # print(app.database.list_collections().to_list())    

    return MongoClient(config["MONGODB_ATLAS_URI"])
    # Load the mongodb database ================================== ================================== stop

# def get_mongodb_collection(db: Database, collection_key:str):
#     return db[collection_key]

def get_user_collection(db:Database):
    return db["user"]

def get_activity_collection(db:Database):
    return db["user_activity"]


## Now, I can't simply pass to the whole nodes. API is becoming big and complex. Hence, I am planning to use Dependency injection

## https://chatgpt.com/c/681f72e4-5ad0-800d-b706-dc2453ab111e
## 👉👉 Finally this is much better. It's following Singleton behavior and things are intact.

class Mongo_Setup(): # Instead of Mongo_Setup, you rename with 
# class DatabaseManager:
    def __init__(self) -> None:
        try:
            # client = MongoClient(config["MONGODB_ATLAS_URI"])
            # self.db = client[""]
            # self._client = MongoClient(config["MONGODB_ATLAS_URI"])
            self._client = None
            self._db = None

            ### 👉 I don't want to create object for collection. Instead I will be happy with methods
            # self._users_collection = None
            # self._user_preferences_collection = None
            # self._compatibility_assessments_collection = None
            # self._trustworthiness_evaluations_collection = None
            # self._match_recommendations_collection = None
            # self._successful_matches_collection = None
            # self._profile_history_collection = None
            # self._message_analytics_collection = None
            # self._user_reports_collection = None
            # self._verification_collection = None
        except:
            raise

    @property
    def db(self):
        # if self._client is None:
        if self._client is None:
            # client = MongoClient(config["MONGODB_ATLAS_URI"])
            client = AsyncMongoClient(config["MONGODB_ATLAS_URI"])
            self._client = client
            self._db = client["my_db"]

            # https://www.perplexity.ai/search/i-am-building-a-dating-app-con-kSPUM6dRTIewbw7RFHglsA
            users_collection = self._db["users"]
            user_preferences_collection = self._db["user_preferences"]
            compatibility_assessments_collection = self._db["compatibility_assessments"]
            trustworthiness_evaluations_collection = self._db["trustworthiness_evaluations"]
            match_recommendations_collection = self._db["match_recommendations"]
            successful_matches_collection = self._db["successful_matches"]
            profile_history_collection = self._db["profile_history"]
            message_analytics_collection = self._db["message_analytics"]
            user_reports_collection = self._db["user_reports"]
            verification_collection = self._db["verification"]

            # Create indexes for performance
            # users_collection.create_index("interests")
            # users_collection.create_index("username")
            # users_collection.create_index("name")
            # compatibility_assessments_collection.create_index([("user_id", 1), ("target_id", 1)])
            # match_recommendations_collection.create_index("user_id")
        return self._db
    
    # @property ## 👉👉 But I don't need any setter.
    def get_users_collection(self):
        if self._db is None:
            raise
        return self._db["users"]
    
    def get_user_preferences_collection(self):
        if self._db is None:
            raise
        return self._db["user_preferences"]
    
    def get_player_collection(self):
        if self._db is None:
            raise
        return self._db["player_collection"]

    def matches(self):
        if self._db is None:
            raise
        return self._db["match_collection"]

def get_mongodb():
    return Mongo_Setup()

mongodb_dependency = Annotated[Mongo_Setup, Depends(get_mongodb)]