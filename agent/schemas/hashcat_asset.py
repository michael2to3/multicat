from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, UUID5, Field


class HashcatAssetSchema(BaseModel):
    task_uuid: Optional[UUID5]
    worker_id: str = Field(min_length=3)
    wordlists: List[str]
    rules: List[str]
    timestamp: datetime

    class Config:
        from_attributes = True
