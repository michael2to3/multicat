from datetime import datetime
from enum import Enum, auto

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from config import Base


class UserRole(Enum):
    ADMIN = auto()
    USER = auto()


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True)
    role = Column(Integer, default=UserRole.USER.value)


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    step_id = Column(Integer, ForeignKey("hashcat_steps.id"))
    user = relationship("User", back_populates="jobs")
    hashes = relationship("Hash", back_populates="job")


User.jobs = relationship("Job", order_by=Job.id, back_populates="user")


step_hashcat_step_association = Table(
    "step_hashcat_step_association",
    Base.metadata,
    Column("step_id", Integer, ForeignKey("steps.id"), primary_key=True),
    Column(
        "hashcat_step_id", Integer, ForeignKey("hashcat_steps.id"), primary_key=True
    ),
)


class Step(Base):
    __tablename__ = "steps"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    hashcat_steps = relationship(
        "HashcatStep", secondary=step_hashcat_step_association, back_populates="steps"
    )


class HashcatStep(Base):
    __tablename__ = "hashcat_steps"
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String)
    steps = relationship(
        "Step", secondary=step_hashcat_step_association, back_populates="hashcat_steps"
    )


class Hash(Base):
    __tablename__ = "hashes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    type_id = Column(Integer, ForeignKey("hash_types.id"))
    value = Column(String)
    cracked_value = Column(String)
    is_cracked = Column(Boolean)
    job = relationship("Job", back_populates="hashes")
    hash_type = relationship("HashType")


class HashType(Base):
    __tablename__ = "hash_types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    hashcat_type = Column(Integer)
    human_readable = Column(String)
