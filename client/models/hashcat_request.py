from datetime import datetime
from enum import Enum, auto

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from config import Base


class UserRole(Enum):
    ADMIN = auto()
    USER = auto()


class JobStatus(Enum):
    CREATED = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True)
    role = Column(Integer, default=UserRole.USER.value)
    assigned_jobs = relationship("Job", order_by="Job.id", back_populates="owning_user")


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Integer, default=JobStatus.CREATED.value)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    step_id = Column(Integer, ForeignKey("hashcat_steps.id"))
    owning_user = relationship("User", back_populates="assigned_jobs")
    associated_hashes = relationship("Hash", back_populates="parent_job")


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
    name = Column(String, unique=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    is_keyspace_calculated = Column(Boolean, default=False)
    hashcat_steps = relationship(
        "HashcatStep",
        secondary=step_hashcat_step_association,
        back_populates="related_steps",
    )


class HashcatStep(Base):
    __tablename__ = "hashcat_steps"
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String)
    related_steps = relationship(
        "Step", secondary=step_hashcat_step_association, back_populates="hashcat_steps"
    )


class Hash(Base):
    __tablename__ = "hashes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String)
    cracked_value = Column(String, nullable=True, default=None)
    is_cracked = Column(Boolean, default=False)
    parent_job = relationship("Job", back_populates="associated_hashes")
    job_id = Column(Integer, ForeignKey("jobs.id"))
    hash_type = relationship("HashType")
    type_id = Column(Integer, ForeignKey("hash_types.id"))


class HashType(Base):
    __tablename__ = "hash_types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    hashcat_type = Column(Integer)
    human_readable = Column(String)
