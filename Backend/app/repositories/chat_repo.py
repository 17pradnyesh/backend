from pymongo import MongoClient
from app.models.chat_model import Chat
import uuid
import os
from datetime import datetime

MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
chats_collection = db["chats"]

def create_chat(chat_data: dict):
    chat_data["chat_id"] = str(uuid.uuid4())
    now = int(datetime.utcnow().timestamp())
    chat_data["created_at"] = now
    chat_data["updated_at"] = now
    result = chats_collection.insert_one(chat_data)
    return str(result.inserted_id)

def get_chat_by_id(chat_id: str):
    return chats_collection.find_one({"chat_id": chat_id})

def update_chat(chat_id: str, update_data: dict):
    update_data["updated_at"] = int(datetime.utcnow().timestamp())
    result = chats_collection.update_one({"chat_id": chat_id}, {"$set": update_data})
    return result.modified_count

def delete_chat(chat_id: str):
    result = chats_collection.delete_one({"chat_id": chat_id})
    return result.deleted_count

def list_chats():
    return list(chats_collection.find())
