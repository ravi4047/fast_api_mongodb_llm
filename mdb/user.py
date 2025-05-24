from fastapi import HTTPException
from pymongo import MongoClient
from pymongo.collection import Collection
from model.player import Player
from model.user import User
## Note, I don't have to create collections or so. It's already will be created.

## This belongs to the user operation.
def get_user(uid:str, dbCollection: Collection):
    user_data = dbCollection.find_one(filter={"_id": uid})
    print("user", user_data)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return User(user_data)

def get_user_birthday(dbCollection:Collection, uid:str):

    return

