from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Agent(BaseModel):
    agent_id: str = Field(..., description="UUID for the agent")
    description: Optional[str] = None
    system_instruction: Optional[str] = None
    is_active: bool = True
    created_at: int = Field(default_factory=lambda: int(datetime.utcnow().timestamp()))
    created_by: Optional[str] = None
    updated_at: Optional[int] = None
