from typing import List, Optional
from pydantic import BaseModel, UUID5, Field
from datetime import datetime


class HashcatAssetSchema(BaseModel):
    id: int
    task_uuid: UUID5
    worker_id: str = Field(min_length=3)
    wordlists: List[str]
    rules: List[str]
    timestamp: datetime

    class Config:
        from_attributes = True
