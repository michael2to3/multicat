from datetime import datetime
from typing import List, Dict, Optional

from pydantic import UUID5, BaseModel, Field


class HashcatAssetSchema(BaseModel):
    id: int
    task_uuid: UUID5
    worker_id: str = Field(min_length=3)
    wordlists: List[str]
    rules: List[str]
    timestamp: datetime
    benchmarks: Optional[Dict]
    devices: Optional[Dict]

    class Config:
        from_attributes = True
