from typing import List
from datetime import datetime
from sqlalchemy import Column, String, create_engine, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
import uuid
from config import Base


class StepsModel(Base):
    __tablename__ = "save_steps"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    owner_id = Column(UUID(as_uuid=True))
    name = Column(String(255), nullable=False)
    steps = Column(JSONB, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
