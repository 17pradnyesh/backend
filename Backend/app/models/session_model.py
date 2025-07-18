from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Session(BaseModel):
    session_id: str = Field(..., description="UUID for the session")
    description: Optional[str] = None
    is_active: bool = True
    created_at: int = Field(default_factory=lambda: int(datetime.utcnow().timestamp()))
    created_by: Optional[str] = None
    updated_at: Optional[int] = None
