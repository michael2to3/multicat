from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from config import Base


class Keyspace(Base):
    __tablename__ = "keyspaces"
    id = Column(Integer, primary_key=True, autoincrement=True)
    attack_mode = Column(String)
    type = Column(String)
    value = Column(Integer)

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "keyspace",
    }


class KeyspaceStraight(Keyspace):
    __mapper_args__ = {"polymorphic_identity": "keyspacestraight"}
    wordlist1: Mapped[str] = mapped_column(use_existing_column=True, nullable=True)
    rule = Column(String, nullable=True)


class KeyspaceCombinator(Keyspace):
    __mapper_args__ = {"polymorphic_identity": "keyspacecombinator"}
    wordlist1: Mapped[str] = mapped_column(use_existing_column=True, nullable=True)
    wordlist2 = Column(String)
    left = Column(String)
    right = Column(String)


class KeyspaceMask(Keyspace):
    __mapper_args__ = {"polymorphic_identity": "keyspacemask"}
    mask: Mapped[str] = mapped_column(use_existing_column=True, nullable=True)
    custom_charsets: Mapped[dict[int, str]] = mapped_column(
        type_=JSONB, use_existing_column=True, nullable=True
    )


class KeyspaceHybrid(Keyspace):
    __mapper_args__ = {"polymorphic_identity": "keyspacehybrid"}
    wordlist1: Mapped[str] = mapped_column(use_existing_column=True, nullable=True)
    mask: Mapped[str] = mapped_column(use_existing_column=True, nullable=True)
    custom_charsets: Mapped[dict[int, str]] = mapped_column(
        type_=JSONB, use_existing_column=True, nullable=True
    )
    wordlist_mask = Column(Boolean)
