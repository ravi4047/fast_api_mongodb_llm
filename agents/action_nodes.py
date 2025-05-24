from state import ConversationGraphState
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from datetime import datetime
import logging
from pymongo.database import Database

## 👉 Is this necessary? 
# Setup logging
logger = logging.getLogger(__name__)

# https://claude.ai/chat/fc84041b-e46b-4bc8-aa34-4334a48ef0b5
async def personal_task_action_node(state: ConversationGraphState, llm: ChatGroq):
    """Handle requests for personal tasks or reminders"""

    # First, determine if this is creating a new task or querying existing ones
    system_prompt = """You are an AI assistant for a dating app that helps users manage their tasks.
    Analyze this message and determine if the user is:
    1. Creating a new task
    2. Updating an existing task
    3. Querying information about their tasks
    4. Deleting a task
    
    Respond with ONLY one of these labels: "create", "update", "query", or "delete".
    """

    messages = [
        SystemMessage(system_prompt),
        HumanMessage(content=f"User message: {state.current_message}")
    ]

    # Get the task action type
    response = await llm.ainvoke(messages)
    task_action = response.content.__str__().strip().lower()

    # Add context for response generation
    context = state.context.copy()
    context.update({
        "task_action": task_action,
        "request_type": "personal_task"
    })

    # Define database operations based on the request
    db_operations = state.db_operations.copy()

    if task_action == "create":
        # Extract task details using LLM
        task_extraction_prompt = """Extract the following task details from the user message:
        - title: The main title of the task
        - description: Any additional description
        - due_date: Any mentioned due date or deadline (format as YYYY-MM-DD if present)
        - priority: The priority level (low, medium, high) if mentioned
        - tags: Any tags or categories mentioned
        
        Respond in JSON format with these fields.
        """

        task_messages = [
            SystemMessage(content=task_extraction_prompt),

            ## 👉 SHould we write like this? I mean explicitly telling User message to the HumanMessage.
            HumanMessage(content=f"User message: {state.current_message}")
        ]

    elif task_action == "query":
        # Default query to get all user tasks, sorted by due date
        db_operations.append({
            "operation": "find",
            "collection": TASKS_COLLECTION,
            "query": {"user_id": state.user_id},
            "sort": [("due_date", 1)],
            "limit": 5
        })
        context["operation"] = "query_tasks"
        
    elif task_action == "update":
        # Extract task identifier
        task_identifier_prompt = """Extract the task identifier (title or description) 
        that the user wants to update from their message.
        
        Respond with ONLY the task identifier text.
        """
        
        task_id_messages = [
            SystemMessage(content=task_identifier_prompt),
            HumanMessage(content=f"User message: {state.current_message}")
        ]
        
        task_id_response = await llm.ainvoke(task_id_messages)
        task_identifier = task_id_response.content.__str__().strip()
        
        # Get the task to update
        db_operations.append({
            "operation": "find_one",
            "collection": TASKS_COLLECTION,
            "query": {
                "user_id": state.user_id,
                "title": {"$regex": f"{task_identifier}", "$options": "i"}
            }
        })
        
        context["task_identifier"] = task_identifier
        context["operation"] = "update_task"
        
    elif task_action == "delete":
        # Extract task identifier
        task_identifier_prompt = """Extract the task identifier (title or description) 
        that the user wants to delete from their message.
        
        Respond with ONLY the task identifier text.
        """
        
        task_id_messages = [
            SystemMessage(content=task_identifier_prompt),
            HumanMessage(content=f"User message: {state.current_message}")
        ]
        
        task_id_response = await llm.ainvoke(task_id_messages)
        task_identifier = task_id_response.content.__str__().strip()
        
        context["task_identifier"] = task_identifier
        context["operation"] = "delete_task"
    
    return ConversationGraphState(
        **state.model_dump(),
        db_operations=db_operations,
        context=context
    )


## General conversation node
async def general_conversation_node(state: ConversationGraphState, llm: ChatGroq)->ConversationGraphState:
    """Handle general conversation that doesn't fit other intents"""

    system_prompt = """You are an AI assistant for a dating app. 
    Your name is Cupid. You are friendly, helpful, and empathetic.
    Keep responses concise and conversational, while still being helpful.
    Avoid giving romantic advice unless explicitly asked.
    
    You may need to help users navigate the dating app, but don't mention specific UI elements
    unless the user is clearly asking about app functionality.
    
    If users seem frustrated or confused, recommend they contact support.
    """
    
    # Format conversation history for context
    conversation_context = ""
    for msg in state.conversation_history[-5]: ## Last 5 messages for context
        role = "User" if msg.get("role") == "user" else "Assistant"
        conversation_context += f"{role}: {msg.get('content')}\n"

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Conversation history:\n{conversation_context}\n\nCurrent message: {state.current_message}")
    ]

    # Generate a conversational response
    response = await llm.ainvoke(messages)
    
    return ConversationGraphState(
        **state.model_dump(),
        response=response.content.__str__(),
    )

### These 3 leftovers need more prompting

# https://claude.ai/chat/2d35617a-0e2f-41a2-9e99-c53207da1d89
# Profile info action node
# async def profile_info_action_node(state: Dict[str, Any]) -> Dict[str, Any]:
async def profile_info_action_node(state: ConversationGraphState) -> ConversationGraphState:

    """
    Processes profile information requests and fetches data from the database.
    """
    logger.info(f"Processing profile info request for conversation: {state.conversation_id}")
    
    try:
        # Extract user ID and target user info from entities
        # user_id = state["user_id"]
        
        # Default to the requesting user if no target is specified
        target_user_id = state.user_id
        requested_fields = ["name", "age", "location", "interests"]  # Default fields
        
        # Look for target user in entities
        for entity in state.get("entities", {}).get("entities", []):
            if entity.type == "user":
                target_user_id = entity.value
            elif entity.type == "profile_field":
                if not isinstance(requested_fields, list):
                    requested_fields = []
                requested_fields.append(entity.value)
        
        # Check permissions (users can only view profiles they've matched with or their own)
        if target_user_id != state.user_id:
            # Check if there's a match between these users
            matches_collection = get_mongodb_collection("matches")
            match = await matches_collection.find_one({
                "$or": [
                    {"user1_id": user_id, "user2_id": target_user_id},
                    {"user1_id": target_user_id, "user2_id": user_id}
                ],
                "status": "active"
            })
            
            if not match:
                return {
                    **state,
                    "response": "Sorry, you can only view profiles of users you've matched with.",
                    "db_operations": state.get("db_operations", []) + [{"operation": "match_check", "result": "failed"}]
                }
        
        # Fetch profile information
        users_collection = get_mongodb_collection("users")
        user_profile = await users_collection.find_one(
            {"_id": target_user_id},
            {"_id": 0, **{field: 1 for field in requested_fields}}
        )
        
        if not user_profile:
            return {
                **state,
                "response": f"I couldn't find profile information for that user.",
                "db_operations": state.get("db_operations", []) + [{"operation": "profile_fetch", "result": "not_found"}]
            }
        
        # Format the response
        response_parts = []
        for field, value in user_profile.items():
            if field == "birthday" and isinstance(value, datetime):
                response_parts.append(f"{field.capitalize()}: {value.strftime('%B %d')}")
            elif field == "interests" and isinstance(value, list):
                response_parts.append(f"{field.capitalize()}: {', '.join(value)}")
            else:
                response_parts.append(f"{field.capitalize()}: {value}")
        
        response = f"Here's the profile information: {'; '.join(response_parts)}"
        
        # Add interaction to user activity log
        activity_collection = get_mongodb_collection("user_activity")
        await activity_collection.insert_one({
            # "user_id": user_id,
            "user_id": state.user_id,
            "action": "profile_view",
            "target_user_id": target_user_id,
            "timestamp": datetime.now()
        })
        
        return {
            **state,
            "response": response,
            "context": {**state.get("context", {}), "profile_info": user_profile},
            "db_operations": state.get("db_operations", []) + [{"operation": "profile_fetch", "result": "success"}]
        }
        
    except Exception as e:
        logger.error(f"Error in profile_info_action_node: {str(e)}")
        return {
            **state,
            "response": "I encountered an issue retrieving that profile information. Please try again later.",
            "error": str(e),
            "db_operations": state.get("db_operations", []) + [{"operation": "profile_fetch", "result": "error", "details": str(e)}]
        }

# Message info action node
# async def message_info_action_node(state: Dict[str, Any]) -> Dict[str, Any]:
async def message_info_action_node(state: ConversationGraphState, db: Database) -> ConversationGraphState:
    """
    Processes message information requests and fetches relevant messages from the database.
    """
    # logger.info(f"Processing message info request for conversation: {state['conversation_id']}")
    logger.info(f"Processing message info request for conversation: {state.conversation_id}")
    
    try:
        # Extract user ID and relevant entities
        # user_id = state["user_id"]
        
        # Initialize variables
        target_user_id = None
        conversation_id = None
        time_range = None
        limit = 5  # Default limit
        
        # Extract entities
        for entity in state.get("entities", {}).get("entities", []):
            if entity.type == "user":
                target_user_id = entity.value
            elif entity.type == "conversation":
                conversation_id = entity.value
            elif entity.type == "number" and entity.name == "limit":
                try:
                    limit = int(entity.value)
                except ValueError:
                    limit = 5
            elif entity.type == "date" and entity.name == "since":
                if not time_range:
                    time_range = {}
                time_range["start"] = datetime.fromisoformat(entity.value)
        
        # Build the query
        query = {"participants": state.user_id}
        
        if target_user_id:
            query["participants"] = {"$all": [user_id, target_user_id]}
        
        if conversation_id:
            query["_id"] = conversation_id
            
        # Fetch conversation data
        conversations_collection = get_mongodb_collection("conversations")
        
        # First find relevant conversations
        if conversation_id:
            conversation = await conversations_collection.find_one(query)
            conversations = [conversation] if conversation else []
        else:
            conversations_cursor = conversations_collection.find(query).sort("last_message_time", -1).limit(5)
            conversations = await conversations_cursor.to_list(length=5)
        
        if not conversations:
            return {
                **state,
                "response": "I couldn't find any messages matching your request.",
                "db_operations": state.get("db_operations", []) + [{"operation": "message_fetch", "result": "not_found"}]
            }
        
        # Now fetch messages for each conversation
        messages_collection = get_mongodb_collection("messages")
        all_messages = []
        
        for conversation in conversations:
            message_query = {"conversation_id": conversation["_id"]}
            
            if time_range and "start" in time_range:
                message_query["timestamp"] = {"$gte": time_range["start"]}
                
            messages_cursor = messages_collection.find(message_query).sort("timestamp", -1).limit(limit)
            conversation_messages = await messages_cursor.to_list(length=limit)
            all_messages.extend(conversation_messages)
        
        # Sort all messages by timestamp
        all_messages.sort(key=lambda x: x["timestamp"], reverse=True)
        if len(all_messages) > limit:
            all_messages = all_messages[:limit]
        
        # Format the response
        if not all_messages:
            response = "I found the conversation, but there are no messages in the specified time range."
        else:
            # Build a summary response
            response = f"I found {len(all_messages)} message{'s' if len(all_messages) != 1 else ''}"
            
            if target_user_id:
                # Get the target user's name
                users_collection = get_mongodb_collection("users")
                target_user = await users_collection.find_one({"_id": target_user_id})
                if target_user and "name" in target_user:
                    response += f" with {target_user['name']}"
                else:
                    response += f" with that user"
            
            if len(all_messages) > 0:
                response += f". The most recent message was sent on {all_messages[0]['timestamp'].strftime('%B %d at %H:%M')}."
                
                # Add a brief summary of the latest message
                sender_id = all_messages[0]["sender_id"]
                # sender_is_user = sender_id ==  user_id
                sender_is_user = sender_id ==  state.user_id

                sender_prefix = "You" if sender_is_user else "They"
                
                # Truncate message content if too long
                content = all_messages[0]["content"]
                if len(content) > 50:
                    content = content[:47] + "..."
                
                response += f" {sender_prefix} said: \"{content}\""
        
        # Log this interaction
        activity_collection = get_mongodb_collection("user_activity")
        await activity_collection.insert_one({
            # "user_id": user_id,
            "user_id": state.user_id,
            "action": "message_info_request",
            "target_user_id": target_user_id,
            "conversation_id": conversation_id,
            "timestamp": datetime.now()
        })
        
        return {
            **state,
            "response": response,
            "context": {**state.get("context", {}), "messages": all_messages},
            "db_operations": state.get("db_operations", []) + [{"operation": "message_fetch", "result": "success"}]
        }
        
    except Exception as e:
        logger.error(f"Error in message_info_action_node: {str(e)}")
        return {
            **state,
            "response": "I encountered an issue retrieving those messages. Please try again later.",
            "error": str(e),
            "db_operations": state.get("db_operations", []) + [{"operation": "message_fetch", "result": "error", "details": str(e)}]
        }

# Match info action node
# async def match_info_action_node(state: Dict[str, Any]) -> Dict[str, Any]:
async def match_info_action_node(state: ) -> Dict[str, Any]:
    """
    Processes match information requests and retrieves data about user matches.
    """
    logger.info(f"Processing match info request for conversation: {state['conversation_id']}")
    
    try:
        # Extract user ID and relevant entities
        user_id = state["user_id"]
        
        # Initialize variables
        match_status = "all"  # Default to all matches
        limit = 5  # Default limit
        sort_by = "last_interaction"  # Default sort
        
        # Parse entities to determine request details
        for entity in state.get("entities", {}).get("entities", []):
            if entity.type == "match_status":
                match_status = entity.value
            elif entity.type == "number" and entity.name == "limit":
                try:
                    limit = int(entity.value)
                except ValueError:
                    limit = 5
            elif entity.type == "sort_criteria":
                sort_by = entity.value
        
        # Build the database query
        query = {
            "$or": [
                {"user1_id": user_id},
                {"user2_id": user_id}
            ]
        }
        
        if match_status == "new":
            query["status"] = "new"
            query["seen_by"] = {"$ne": user_id}
        elif match_status == "active":
            query["status"] = "active"
        elif match_status != "all":
            query["status"] = match_status
        
        # Define sort criteria
        sort_criteria = []
        if sort_by == "recent":
            sort_criteria.append(("created_at", -1))
        elif sort_by == "last_interaction":
            sort_criteria.append(("last_interaction", -1))
        else:
            sort_criteria.append(("created_at", -1))  # Default sort
        
        # Fetch matches from database
        matches_collection = get_mongodb_collection("matches")
        matches_cursor = matches_collection.find(query).sort(sort_criteria).limit(limit)
        matches = await matches_cursor.to_list(length=limit)
        
        if not matches:
            response_by_status = {
                "new": "You don't have any new matches at the moment.",
                "active": "You don't have any active matches right now.",
                "all": "You don't have any matches yet."
            }
            return {
                **state,
                "response": response_by_status.get(match_status, "No matches found matching your criteria."),
                "db_operations": state.get("db_operations", []) + [{"operation": "match_fetch", "result": "not_found"}]
            }
        
        # Get user information for all matched users
        users_collection = get_mongodb_collection("users")
        match_user_ids = []
        
        for match in matches:
            other_user_id = match["user1_id"] if match["user1_id"] != user_id else match["user2_id"]
            match_user_ids.append(other_user_id)
        
        matched_users = {}
        users_cursor = users_collection.find({"_id": {"$in": match_user_ids}})
        
        async for user in users_cursor:
            matched_users[user["_id"]] = user
        
        # Format the response
        if match_status == "new":
            response = f"You have {len(matches)} new match{'es' if len(matches) != 1 else ''}!"
        else:
            response = f"You have {len(matches)} match{'es' if len(matches) != 1 else ''}."
        
        # Add some details about the matches
        if len(matches) > 0:
            match_details = []
            
            for i, match in enumerate(matches[:3]):  # Show details for up to 3 matches
                other_user_id = match["user1_id"] if match["user1_id"] != user_id else match["user2_id"]
                other_user = matched_users.get(other_user_id, {})
                
                user_name = other_user.get("name", "Someone")
                user_age = other_user.get("age", "")
                user_location = other_user.get("location", "")
                
                match_info = user_name
                if user_age:
                    match_info += f", {user_age}"
                if user_location:
                    match_info += f" from {user_location}"
                
                match_details.append(match_info)
            
            if match_details:
                if len(matches) <= 3:
                    response += f" Your matches include: {', '.join(match_details)}."
                else:
                    response += f" Your top matches include: {', '.join(match_details)}, and {len(matches) - 3} more."
        
        # Mark new matches as seen
        if match_status == "new":
            update_result = await matches_collection.update_many(
                {
                    "$or": [
                        {"user1_id": user_id},
                        {"user2_id": user_id}
                    ],
                    "status": "new",
                    "seen_by": {"$ne": user_id}
                },
                {"$addToSet": {"seen_by": user_id}}
            )
        
        # Log this interaction
        activity_collection = get_mongodb_collection("user_activity")
        await activity_collection.insert_one({
            "user_id": user_id,
            "action": "match_info_request",
            "match_status": match_status,
            "timestamp": datetime.now()
        })
        
        return {
            **state,
            "response": response,
            "context": {**state.get("context", {}), "matches": matches, "matched_users": matched_users},
            "db_operations": state.get("db_operations", []) + [{"operation": "match_fetch", "result": "success"}]
        }
        
    except Exception as e:
        logger.error(f"Error in match_info_action_node: {str(e)}")
        return {
            **state,
            "response": "I encountered an issue retrieving your matches. Please try again later.",
            "error": str(e),
            "db_operations": state.get("db_operations", []) + [{"operation": "match_fetch", "result": "error", "details": str(e)}]
        }