from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY, UUID

from config import Base


class HashcatAsset(Base):
    __tablename__ = "assets"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_uuid = Column(UUID(as_uuid=True))
    worker_id = Column(String, nullable=False)
    files = Column(ARRAY(String))
    created_at = Column(DateTime(timezone=True), default=datetime.now(UTC))
