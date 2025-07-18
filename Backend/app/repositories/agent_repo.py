from pymongo import MongoClient
from app.models.agent_model import Agent
from bson import ObjectId
import uuid
import os
from datetime import datetime

MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
agents_collection = db["agents"]

def create_agent(agent_data: dict):
    agent_data["agent_id"] = str(uuid.uuid4())
    now = int(datetime.utcnow().timestamp())
    agent_data["created_at"] = now
    agent_data["updated_at"] = now
    result = agents_collection.insert_one(agent_data)
    return str(result.inserted_id)

def get_agent_by_id(agent_id: str):
    return agents_collection.find_one({"agent_id": agent_id})

def update_agent(agent_id: str, update_data: dict):
    update_data["updated_at"] = int(datetime.utcnow().timestamp())
    result = agents_collection.update_one({"agent_id": agent_id}, {"$set": update_data})
    return result.modified_count

def delete_agent(agent_id: str):
    result = agents_collection.delete_one({"agent_id": agent_id})
    return result.deleted_count

def list_agents():
    return list(agents_collection.find())
