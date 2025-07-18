from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class File(BaseModel):
    file_id: str = Field(..., description="UUID for the file")
    chat_id: str
    file_name: str
    mimetype: str
    file_size: str
    size_type: str
    upload_path: str
    download_url: str
    created_at: int = Field(default_factory=lambda: int(datetime.utcnow().timestamp()))
