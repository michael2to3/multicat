from datetime import datetime

from config import Base
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import JSONB


class Devices(Base):
    __tablename__ = "devices"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    worker_name = Column(String, nullable=False)
    value = Column(JSONB, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
