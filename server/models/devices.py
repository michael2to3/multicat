from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

from config import Base


class Devices(Base):
    __tablename__ = "devices"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    worker_name = Column(String, nullable=False)
    value = Column(JSONB, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(UTC))
