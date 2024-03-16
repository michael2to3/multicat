from typing import List
from datetime import datetime
from sqlalchemy import Column, String, create_engine, DateTime
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid
from config import Base


class HashcatAsset(Base):
    __tablename__ = "worker"
    __table_args__ = {"extend_existing": True}

    task_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    worker_id = Column(String, nullable=False)
    wordlists = Column(ARRAY(String))
    rules = Column(ARRAY(String))
    timestamp = Column(DateTime, default=datetime.utcnow)
