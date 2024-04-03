from datetime import datetime

from config import Base
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey


class Benchmark(Base):
    __tablename__ = "benchmarks"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    worker_name = Column(String, nullable=False)
    hash_type_id = Column(Integer, ForeignKey("hash_types.id"))
    value = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
