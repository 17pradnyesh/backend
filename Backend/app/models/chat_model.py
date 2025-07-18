from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Chat(BaseModel):
    chat_id: str = Field(..., description="UUID for the chat")
    session_id: str
    agent_id: str
    message: str
    type: str  # user / model
    contain_files: bool = False
    created_at: int = Field(default_factory=lambda: int(datetime.utcnow().timestamp()))
    updated_at: Optional[int] = None
