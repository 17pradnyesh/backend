
from pymongo import MongoClient
import uuid
import os
from datetime import datetime

MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
sessions_collection = db["sessions"]

def create_session(session_data: dict):
    session_data["session_id"] = str(uuid.uuid4())
    now = int(datetime.utcnow().timestamp())
    session_data["created_at"] = now
    session_data["updated_at"] = now
    result = sessions_collection.insert_one(session_data)
    return str(result.inserted_id)

def get_session_by_id(session_id: str):
    return sessions_collection.find_one({"session_id": session_id})

def update_session(session_id: str, update_data: dict):
    update_data["updated_at"] = int(datetime.utcnow().timestamp())
    result = sessions_collection.update_one({"session_id": session_id}, {"$set": update_data})
    return result.modified_count

def delete_session(session_id: str):
    result = sessions_collection.delete_one({"session_id": session_id})
    return result.deleted_count

def list_sessions():
    return list(sessions_collection.find())