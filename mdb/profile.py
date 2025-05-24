from fastapi import Depends
from pymongo import collection
from setup import get_mongodb, Mongo_Setup

async def search_profile_by_name(name:str, user_id:str, mdb_setup: Mongo_Setup = Depends(get_mongodb)):
    result = await mdb_setup.get_users_collection().find_one(filter={"name": user_id})
    print(result)
    return result


async def get_profile_by_id(profile_id: str, mdb_setup: Mongo_Setup = Depends(get_mongodb)):
    # ans = mdb_setup.get_player_collection().find_one(filter={"_id": profile_id}) # 🤔
    ## For async/await you need AsyncMongoClient and not MongoClient.
    # --------------------------------------------- ------------------------------------------- START
    ## 👉👉👉🤔🤔🤔 Why are they using async one?
#     When to Use Each Approach:
# Use Async When:

# High concurrency requirements (dating apps, social media)
# Many I/O operations (database, API calls)
# Real-time features (chat, notifications)
# Modern web applications

# Use Sync When:

# Simple CRUD applications with low traffic
# CPU-intensive tasks (data processing, calculations)
# Legacy systems integration
# Simpler debugging requirements

# Performance Impact Example:
# python# Sync: 100 users chatting = 100 threads = high memory usage
# # Each request blocks for 3+ seconds

# # Async: 100 users chatting = 1 thread = low memory usage  
# # Requests are processed concurrently while waiting for I/O
# For a dating app with potentially thousands of users browsing, chatting, and matching simultaneously, async is almost essential for good performance. 
# But if you prefer sync code for simplicity and don't expect high concurrency, the sync approach would work too!
# --------------------------------------------- ------------------------------------------- STOP

    """Get profile by ID."""
    ans = await mdb_setup.get_player_collection().find_one(filter={"_id": profile_id}) # Now converted to AsyncMongoClient so now can use await

    return ans


