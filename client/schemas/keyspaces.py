import logging
from abc import abstractmethod
from typing import List, Literal, Tuple

from pydantic import BaseModel, validator

from hashcat.configurer import IHashcatConfigurer
from schemas import AttackMode
from schemas.hashcat_request import CustomCharset

logger = logging.getLogger(__name__)


class KeyspaceBase(BaseModel):
    attack_mode: AttackMode
    value: int

    @classmethod
    def get_subclasses(cls) -> Tuple:
        return tuple(cls.__subclasses__())

    @abstractmethod
    def accept(self, configurer: IHashcatConfigurer):
        pass

    class Config:
        from_attributes = True
        fields = {"attack_mode": {"exclude": True}}


class KeyspaceStraightSchema(KeyspaceBase):
    attack_mode: AttackMode = AttackMode.DICTIONARY
    wordlist1: str
    rule: str
    type: Literal["keyspacestraight"] = "keyspacestraight"

    def accept(self, configurer: IHashcatConfigurer):
        configurer.configure_straight(self)


class KeyspaceCombinatorSchema(KeyspaceBase):
    attack_mode: AttackMode = AttackMode.COMBINATOR
    wordlist1: str
    wordlist2: str
    left: str
    right: str
    type: Literal["keyspacecombinator"] = "keyspacecombinator"

    def accept(self, configurer: IHashcatConfigurer):
        configurer.configure_combinator(self)


class KeyspaceMaskSchema(KeyspaceBase):
    attack_mode: AttackMode = AttackMode.MASK
    mask: str
    custom_charsets: List[CustomCharset]
    type: Literal["keyspacemask"] = "keyspacemask"

    def accept(self, configurer: IHashcatConfigurer):
        configurer.configure_mask(self)


class KeyspaceHybridSchema(KeyspaceBase):
    attack_mode: AttackMode
    wordlist1: str
    mask: str
    wordlist_mask: bool
    type: Literal["keyspacehybrid"] = "keyspacehybrid"

    def accept(self, configurer: IHashcatConfigurer):
        configurer.configure_hybrid(self)

    @validator("attack_mode", pre=True, always=True)
    @classmethod
    def change_attack_mode(cls, v, values) -> AttackMode:
        if v is not None:
            return v

        if cls.wordlist_mask:
            return AttackMode.HYBRID_DICT_MASK

        return AttackMode.HYBRID_MASK_DICT
