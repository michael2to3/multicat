from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from config import Base
from schemas import JobStatus, UserRole


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True)
    role = Column(String, default=UserRole.USER.value)
    pubkey = Column(Text, default="")
    assigned_jobs = relationship("Job", order_by="Job.id", back_populates="owning_user")


job_hash_association = Table(
    "job_hash_association",
    Base.metadata,
    Column("job_id", UUID(as_uuid=True), ForeignKey("jobs.id"), primary_key=True),
    Column("hash_id", Integer, ForeignKey("hashes.id"), primary_key=True),
)


class Job(Base):
    __tablename__ = "jobs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    status = Column(String, default=JobStatus.CREATED.value)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    step_id = Column(Integer, ForeignKey("hashcat_steps.id"))
    owning_user = relationship("User", back_populates="assigned_jobs")
    associated_hashes = relationship(
        "Hash", secondary=job_hash_association, back_populates="related_jobs"
    )


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
    timestamp = Column(DateTime(timezone=True), default=datetime.now(UTC))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    status = Column(String)
    original_content = Column(String)
    hashcat_steps = relationship(
        "HashcatStep",
        secondary=step_hashcat_step_association,
        back_populates="related_steps",
    )


class HashcatStep(Base):
    __tablename__ = "hashcat_steps"
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(JSONB)
    related_steps = relationship(
        "Step", secondary=step_hashcat_step_association, back_populates="hashcat_steps"
    )


class Hash(Base):
    __tablename__ = "hashes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String)
    cracked_value = Column(String, nullable=True, default=None)
    is_cracked = Column(Boolean, default=False)
    related_jobs = relationship(
        "Job", secondary=job_hash_association, back_populates="associated_hashes"
    )
    hash_type = relationship("HashType")
    type_id = Column(Integer, ForeignKey("hash_types.id"))


class HashType(Base):
    __tablename__ = "hash_types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    hashcat_type = Column(Integer)
    human_readable = Column(String)
