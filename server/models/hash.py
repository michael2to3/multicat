from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from config import Base


class HashType(Base):
    __tablename__ = "hash_types"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)


class Hash(Base):
    __tablename__ = "hashes"
    id = Column(Integer, primary_key=True)
    hash_value = Column(String(255))
    hash_type_id = Column(Integer, ForeignKey("hash_types.id"))
    hash_type = relationship("HashType")
