from fastapi import HTTPException
from mdb.db_manager import DatabaseManager
from datetime import datetime

from typing import Optional, Dict, List

import logging

from mdb.db_manager import db_manager ## Note, this must be initialized.

logger = logging.getLogger(__name__)

# Database operations with error handling
class ProfileRepository:
    """Profile-related database operations."""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    async def get_profile_by_id(self, profile_id: str) -> Optional[Dict]:
        """Get profile by ID with error handling."""
        try:
            result = await self.db.profiles.find_one({"_id": profile_id})
            return result
        except Exception as e:
            logger.error(f"Error getting profile {profile_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Database error")
    
    async def search_by_name(self, name: str, limit: int = 10) -> List[Dict]:
        """Search profiles by name with error handling."""
        try:
            cursor = self.db.profiles.find(
                {"name": {"$regex": name, "$options": "i"}}
            ).limit(limit)
            return await cursor.to_list(length=limit)
        except Exception as e:
            logger.error(f"Error searching profiles by name '{name}': {str(e)}")
            raise HTTPException(status_code=500, detail="Database search error")
    
    async def create(self, profile_data: Dict) -> str:
        """Create a new profile."""
        try:
            profile_data["created_at"] = datetime.now()
            profile_data["updated_at"] = datetime.now()
            result = await self.db.profiles.insert_one(profile_data)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error creating profile: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to create profile")
        
# Initialize repositories
profile_repo = ProfileRepository(db_manager)