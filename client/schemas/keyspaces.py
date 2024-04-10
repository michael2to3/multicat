import logging
from abc import ABC, abstractmethod
from typing import Annotated, List, Literal, Union

from pydantic import BaseModel, Field, TypeAdapter, validator

from schemas import AttackMode
from schemas.hashcat_request import CustomCharset
from visitor import IKeyspaceVisitor

logger = logging.getLogger(__name__)


class KeyspaceBase(BaseModel, ABC):
    attack_mode: AttackMode
    value: int

    @classmethod
    def get_subclasses(cls) -> tuple:
        return tuple(cls.__subclasses__())

    @abstractmethod
    def accept(self, configurer: IKeyspaceVisitor):
        pass

    class Config:
        from_attributes = True
        fields = {"attack_mode": {"exclude": True}}


class KeyspaceStraightSchema(KeyspaceBase):
    attack_mode: AttackMode = AttackMode.DICTIONARY
    wordlist1: str
    rule: str
    type: Literal["keyspacestraight"] = "keyspacestraight"

    def accept(self, configurer: IKeyspaceVisitor):
        configurer.configure_straight(self)


class KeyspaceCombinatorSchema(KeyspaceBase):
    attack_mode: AttackMode = AttackMode.COMBINATOR
    wordlist1: str
    wordlist2: str
    left: str
    right: str
    type: Literal["keyspacecombinator"] = "keyspacecombinator"

    def accept(self, configurer: IKeyspaceVisitor):
        configurer.configure_combinator(self)


class KeyspaceMaskSchema(KeyspaceBase):
    attack_mode: AttackMode = AttackMode.MASK
    mask: str
    custom_charsets: List[CustomCharset]
    type: Literal["keyspacemask"] = "keyspacemask"

    def accept(self, configurer: IKeyspaceVisitor):
        configurer.configure_mask(self)


class KeyspaceHybridSchema(KeyspaceBase):
    attack_mode: AttackMode
    wordlist1: str
    mask: str
    wordlist_mask: bool
    type: Literal["keyspacehybrid"] = "keyspacehybrid"

    def accept(self, configurer: IKeyspaceVisitor):
        configurer.configure_hybrid(self)

    @validator("attack_mode", pre=True, always=True)
    @classmethod
    def change_attack_mode(cls, v, values) -> AttackMode:
        if v is not None:
            return v

        if cls.wordlist_mask:
            return AttackMode.HYBRID_DICT_MASK

        return AttackMode.HYBRID_MASK_DICT


def get_keyspace_adapter() -> Annotated:
    return TypeAdapter(
        Annotated[Union[KeyspaceBase.get_subclasses()], Field(discriminator="type")]
    )
