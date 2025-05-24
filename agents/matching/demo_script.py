import asyncio
import json
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Connect to MongoDB
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["dating_app_db"]

# Collections
profiles_collection = db["profiles"]
matches_collection = db["matches"]
messages_collection = db["messages"]
feeds_history_collection = db["feeds_history"]

# Sample data
SAMPLE_PROFILES = [
    {
        "_id": str(ObjectId()),
        "name": "Tanya",
        "age": 28,
        "gender": "female",
        "bio": "Adventure seeker and coffee enthusiast. I love hiking, photography, and trying new restaurants. Looking for someone who shares my passion for outdoor activities and good conversation.",
        "interests": ["hiking", "photography", "coffee", "travel", "cooking"],
        "photos": ["https://example.com/photos/tanya1.jpg", "https://example.com/photos/tanya2.jpg"],
        "location": {"lat": 40.7128, "lng": -74.0060},
        "preferences": {
            "age_min": 26,
            "age_max": 34,
            "distance": 25,
            "gender": "male"
        },
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "_id": str(ObjectId()),
        "name": "Alex",
        "age": 32,
        "gender": "male",
        "bio": "Software engineer by day, musician by night. I enjoy coding, playing guitar, and exploring new technologies. Looking for someone who appreciates good music and interesting conversations about tech or philosophy.",
        "interests": ["music", "coding", "technology", "philosophy", "hiking"],
        "photos": ["https://example.com/photos/alex1.jpg", "https://example.com/photos/alex2.jpg"],
        "location": {"lat": 40.7328, "lng": -74.0060},
        "preferences": {
            "age_min": 25,
            "age_max": 35,
            "distance": 20,
            "gender": "female"
        },
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "_id": str(ObjectId()),
        "name": "Sarah",
        "age": 26,
        "gender": "female",
        "bio": "Art teacher with a passion for painting and sculpture. I love visiting museums, attending art exhibitions, and teaching children about creativity. Looking for someone who values culture and artistic expression.",
        "interests": ["art", "museums", "teaching", "reading", "wine tasting"],
        "photos": ["https://example.com/photos/sarah1.jpg", "https://example.com/photos/sarah2.jpg"],
        "location": {"lat": 40.7228, "lng": -73.9860},
        "preferences": {
            "age_min": 25,
            "age_max": 35,
            "distance": 15,
            "gender": "male"
        },
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "_id": str(ObjectId()),
        "name": "Michael",
        "age": 30,
        "gender": "male",
        "bio": "Fitness coach who loves helping people achieve their health goals. When I'm not at the gym, I enjoy cooking healthy meals, reading psychology books, and going on long runs in the park.",
        "interests": ["fitness", "nutrition", "psychology", "running", "cooking"],
        "photos": ["https://example.com/photos/michael1.jpg", "https://example.com/photos/michael2.jpg"],
        "location": {"lat": 40.7328, "lng": -73.9960},
        "preferences": {
            "age_min": 25,
            "age_max": 32,
            "distance": 20,
            "gender": "female"
        },
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "_id": str(ObjectId()),
        "name": "Emma",
        "age": 29,
        "gender": "female",
        "bio": "Veterinarian and animal lover. I spend my days caring for pets and my free time volunteering at animal shelters. Looking for someone who shares my love for animals and nature.",
        "interests": ["animals", "nature", "volunteering", "reading", "hiking"],
        "photos": ["https://example.com/photos/emma1.jpg", "https://example.com/photos/emma2.jpg"],
        "location": {"lat": 40.7028, "lng": -74.0160},
        "preferences": {
            "age_min": 27,
            "age_max": 36,
            "distance": 25,
            "gender": "male"
        },
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
]

# Sample user for testing
TEST_USER = {
    "_id": str(ObjectId()),
    "name": "Test User",
    "age": 31,
    "gender": "male",
    "bio": "Testing the dating app chatbot system. I enjoy various activities and am looking to meet new people.",
    "interests": ["testing", "technology", "travel", "food", "movies"],
    "photos": ["https://example.com/photos/testuser1.jpg", "https://example.com/photos/testuser2.jpg"],
    "location": {"lat": 40.7228, "lng": -74.0060},
    "preferences": {
        "age_min": 25,
        "age_max": 35,
        "distance": 25,
        "gender": "female"
    },
    "created_at": datetime.utcnow(),
    "updated_at": datetime.utcnow()
}