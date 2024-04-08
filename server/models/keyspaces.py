from sqlalchemy import JSON, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Keyspace(Base):
    __tablename__ = "keyspaces"
    id = Column(Integer, primary_key=True, autoincrement=True)
    attack_mode = Column(Integer)
    type = Column(String)
    value = Column(Integer)

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "keyspace",
    }


class KeyspaceStraight(Keyspace):
    wordlist1 = Column(String)
    rule = Column(String)
    __mapper_args__ = {"polymorphic_identity": "keyspacestraight"}


class KeyspaceCombinator(Keyspace):
    wordlist1 = Column(String)
    wordlist2 = Column(String)
    left = Column(String)
    right = Column(String)
    __mapper_args__ = {"polymorphic_identity": "keyspacecombinator"}


class KeyspaceMask(Keyspace):
    mask = Column(String)
    custom_charsets = Column(JSON)
    __mapper_args__ = {"polymorphic_identity": "keyspacemask"}


class KeyspaceHybrid(Keyspace):
    wordlist1 = Column(String)
    mask = Column(String)
    wordlist_mask = Column(bool)
    __mapper_args__ = {"polymorphic_identity": "keyspacehybrid"}
