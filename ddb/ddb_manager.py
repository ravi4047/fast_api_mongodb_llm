from typing import Any, Dict, List
import boto3
from boto3.resources.base import ServiceResource
from boto3.dynamodb.conditions import Key, Attr

from configuration import DDB_REGION_NAME, DDB_ACCESS_KEY_ID, DDB_SECRET_ACCESS_KEY

from model.chat import ChatItem

from datetime import datetime

from model.chat import ChatPagingResult

# https://github.com/agusrichard/devops-workbook/blob/master/fastapi-dynamo/app/internal/db.py

# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
class Dynamo_Manager:
    def __init__(self) -> None:
        self.ddb = boto3.resource('dynamodb', 
                region_name=DDB_REGION_NAME,
                aws_access_key_id=DDB_ACCESS_KEY_ID,
                aws_secret_access_key=DDB_SECRET_ACCESS_KEY)
        # # ddb2 = boto3.client("dynamodb", )

        # dd = self.ddb.Table("Rec")
        # self.ddb2 = self._initialize_db()


    ### 👉👉 This is not required. It doesn't require mongo_db operation. I don't think 
    def _initialize_db(self)->ServiceResource:
        """Initialize database connection."""
        try:
            ddb = boto3.resource('dynamodb', 
                region_name=DDB_REGION_NAME,
                aws_access_key_id=DDB_ACCESS_KEY_ID,
                aws_secret_access_key=DDB_SECRET_ACCESS_KEY)
            self.ddb = ddb
            return ddb
        except Exception as e:
            raise
    
    ## I think I should do paging.
    ## I am doing this. But how.
    def get_chat_messages(self, conv_id:str):
        try:
            message_table = self.ddb.Table("chat")
            response = message_table.query(
                IndexName="chat_timestamp_index",
                KeyConditionExpression=Key("match_id").eq(conv_id),
                Limit=20,
                ScanIndexForward=False
            )

            for key, value in response.items():
                print(key)
                print(value)


        except Exception as e:
            pass

    
    ## For the future Ravi, Paging chat items upto a certain limit or till that last chat id where summary is performed.
    ## If for a certain limit, then all the chats are performed, and then the summary is done and again the paging is repeated 
    ## upto like 100 messages or so.
    def scan_chat_items(self, match_id: str, uid:str, last_key_id: str, last_key_timestamp: int, limit: int = 10, filter_expr=None) -> ChatPagingResult: # -> List[ChatItem]: # List[Dict[str, Any]]:
        scan_kwargs: dict[str, Any] = {"Limit": limit}
        
        # if self.last_evaluated_key:
        #     scan_kwargs["ExclusiveStartKey"] = self.last_evaluated_key

        # if filter_expr:
        #     scan_kwargs["FilterExpression"] = filter_expr

        response = self.ddb.Table("chat").scan(
            IndexName="chat_timestamp_index",
            ExclusiveStartKey={
                "match_id": match_id,
                "id": last_key_id,
                "timestamp": f"{last_key_timestamp}"
            },
            Limit=limit,
        )
        # self.last_evaluated_key = response.get("LastEvaluatedKey") # WHy I should save them?
        # items = response.get("Items", [])

        chatItems = []
        for _, item in response.items():
            chatItems.append(ChatItem.to_chat_item(result=item.__dict__, sender_uid=uid))

        return ChatPagingResult({"chats": chatItems, "end": response.get("LastEvaluatedKey") is not None})