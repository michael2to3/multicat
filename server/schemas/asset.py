from typing import List, Optional
from pydantic import BaseModel, UUID4, Field


class HashcatAssetSchema(BaseModel):
    task_uuid: Optional[UUID4]
    worker_id: str = Field(min_length=3)
    wordlists: List[str]
    rules: List[str]

    class Config:
        orm_mode = True
