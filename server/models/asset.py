from typing import List
from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid


Base = declarative_base()


class HashcatAsset(Base):
    __tablename__ = "worker"

    task_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    worker_id = Column(String, nullable=False)
    wordlists = Column(ARRAY(String))
    rules = Column(ARRAY(String))
