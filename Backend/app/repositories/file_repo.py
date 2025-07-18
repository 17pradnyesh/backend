from pymongo import MongoClient
from app.models.file_model import File
import uuid
import os
from datetime import datetime

MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
files_collection = db["files"]

def create_file(file_data: dict):
    file_data["file_id"] = str(uuid.uuid4())
    now = int(datetime.utcnow().timestamp())
    file_data["created_at"] = now
    result = files_collection.insert_one(file_data)
    return str(result.inserted_id)

def get_file_by_id(file_id: str):
    return files_collection.find_one({"file_id": file_id})

def update_file(file_id: str, update_data: dict):
    update_data["updated_at"] = int(datetime.utcnow().timestamp())
    result = files_collection.update_one({"file_id": file_id}, {"$set": update_data})
    return result.modified_count

def delete_file(file_id: str):
    result = files_collection.delete_one({"file_id": file_id})
    return result.deleted_count

def list_files():
    return list(files_collection.find())
