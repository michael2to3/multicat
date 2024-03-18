import uuid
from datetime import datetime
from typing import List

from config import Base
from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.dialects.postgresql import ARRAY, UUID


class HashcatAsset(Base):
    __tablename__ = "worker"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_uuid = Column(UUID(as_uuid=True))
    worker_id = Column(String, nullable=False)
    wordlists = Column(ARRAY(String))
    rules = Column(ARRAY(String))
    timestamp = Column(DateTime, default=datetime.utcnow)
