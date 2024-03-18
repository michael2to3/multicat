import uuid
from datetime import datetime
from typing import List

from config import Base
from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID


class StepsModel(Base):
    __tablename__ = "save_steps"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    owner_id = Column(UUID(as_uuid=True))
    name = Column(String(255), nullable=False)
    steps = Column(JSONB, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
