from datetime import datetime
from typing import List

from pydantic import UUID5, BaseModel, Field


class HashcatAssetSchema(BaseModel):
    id: int
    task_uuid: UUID5
    worker_id: str = Field(min_length=3)
    files: List[str]
    timestamp: datetime

    class Config:
        from_attributes = True
