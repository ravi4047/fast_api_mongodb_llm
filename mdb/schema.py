# User schema with matching-related fields
user_schema = {
    "_id": "uuid",
    "name": "string",
    "bio": "string",
    "interests": ["array of strings"],
    "preferences": {
        "age_range": [min, max],
        "interests": ["array of strings"],
        "location_preference": "string"
    },
    "behavior_metrics": {
        "response_rate": "float",
        "profile_completeness": "float",
        "reported_count": "integer"
    }
}

# Matches collection schema
match_schema = {
    "_id": "uuid",
    "user_id": "uuid",
    "target_id": "uuid",
    "status": "string",  # "pending", "approved", "rejected"
    "compatibility_score": "float",
    "created_at": "timestamp",
    "updated_at": "timestamp"
}