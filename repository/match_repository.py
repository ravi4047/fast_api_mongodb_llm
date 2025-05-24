from fastapi import HTTPException
from datetime import datetime
# from mdb.setup import DatabaseManager
from mdb.db_manager import DatabaseManager

from mdb.db_manager import db_manager ## Note, this must be initialized.
import logging

logger = logging.getLogger(__name__)

### ------------------------------------------------------------------------ START --------------------------------------
# My Recommendation: Approach 1 (Database Manager Class)
# Why this is the best approach:

# No DI Overhead: You don't need to pass database dependencies to every function
# Centralized Connection Management: Single place to handle connections, errors, and lifecycle
# Easy Testing: You can mock the entire db_manager
# Error Handling: Built-in error handling with proper logging
# Repository Pattern: Clean separation of concerns
# Lifecycle Management: Proper startup/shutdown handling

# Comparison Table
# ApproachProsConsBest ForGlobal Connection (Original)Simple, fastNo error handling, hard to testSmall apps, prototypesDatabase Manager (Recommended)Best of all worldsSlightly more complexProduction appsPure DIVery testableDI everywhere, verboseEnterprise appsContext ManagerSafe connectionsNew connection per requestLow-traffic apps
# For Your Dating App:

# Use Database Manager approach - it gives you all the benefits without DI complexity
# Add proper error handling - users shouldn't see database errors
# Use lifespan management - ensures clean startup/shutdown
# Repository pattern - makes testing and maintenance easier

# The Database Manager approach eliminates your main concern (passing database as DI everywhere) while still providing proper connection management, error handling, and testability. You get clean, simple function calls like:
# pythonprofile = await profile_repo.get_by_id("123")
# matches = await match_repo.get_user_matches("123")
### ------------------------------------------------------------------------ STOP --------------------------------------

## Repository pattern is 
class MatchRepository:
    """Match related database operations"""

    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db = db_manager

    async def get_user_matches(self, user_id:str):
        """Get all matches for a user"""
        try:
            result = await self.db.feeds_history.find_one(filter={"user": 234})
            return result
        except Exception as e:
            logger.error(f"Error adding feed message: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to save matches")

    async def create_match(self, user1_id: str, user2_id: str) -> str:
        """Create a new match."""
        try:
            match_data = {
                "user1_id": user1_id,
                "user2_id": user2_id,
                "status": "pending",
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
            result = await self.db.matches.insert_one(match_data)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error creating match: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to create match")
        
# Initialize repositories
match_repo = MatchRepository(db_manager)