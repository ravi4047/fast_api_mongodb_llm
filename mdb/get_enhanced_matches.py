from typing import Any, Dict, List

# https://claude.ai/chat/bd16e0ac-f26c-4874-96da-dfa0b3b534e0
async def get_enhanced_matches(self, user_id: str, filters: Dict[str, Any]|None = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Enhanced matching with compatibility scoring"""
        user_profile = await self.get_user_profile(user_id)
        if not user_profile:
            return []
            
        # Build query
        query = {"id": {"$ne": user_id}}
        
        # Age range
        age_min = filters.get("age_min", user_profile.get("age", 25) - 5)
        age_max = filters.get("age_max", user_profile.get("age", 25) + 5)
        query["age"] = {"$gte": age_min, "$lte": age_max}
        
        # Location (if specified)
        if filters.get("location"):
            query["location"] = filters["location"]
        elif user_profile.get("location"):
            query["location"] = user_profile["location"]
        
        # Common interests
        if user_profile.get("interests"):
            query["interests"] = {"$in": user_profile["interests"]}
            
        cursor = self.profiles.find(query).limit(limit * 2)  # Get more for scoring
        potential_matches = await cursor.to_list(length=limit * 2)
        
        # Score matches
        scored_matches = []
        user_interests = set(user_profile.get("interests", []))
        
        for match in potential_matches:
            match_interests = set(match.get("interests", []))
            common_interests = user_interests.intersection(match_interests)
            
            # Simple compatibility scoring
            compatibility = len(common_interests) / max(len(user_interests), 1)
            
            # Age compatibility bonus
            age_diff = abs(user_profile.get("age", 25) - match.get("age", 25))
            age_bonus = max(0, (10 - age_diff) / 10) * 0.2
            
            final_score = min(1.0, compatibility + age_bonus)
            
            match["compatibility_score"] = final_score
            match["common_interests"] = list(common_interests)
            scored_matches.append(match)
        
        # Sort by compatibility and return top matches
        scored_matches.sort(key=lambda x: x["compatibility_score"], reverse=True)
        return scored_matches[:limit]