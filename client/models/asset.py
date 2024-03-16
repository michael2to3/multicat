from typing import List
from datetime import datetime
from sqlalchemy import Column, String, create_engine, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid
from config import Base


class HashcatAsset(Base):
    __tablename__ = "worker"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_uuid = Column(UUID(as_uuid=True))
    worker_id = Column(String, nullable=False)
    wordlists = Column(ARRAY(String))
    rules = Column(ARRAY(String))
    timestamp = Column(DateTime, default=datetime.utcnow)
