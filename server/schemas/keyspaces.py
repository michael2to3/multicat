from typing import List, Literal

from pydantic import BaseModel


class KeyspaceBase(BaseModel):
    attack_mode: int
    value: int

    class Config:
        from_attributes = True


class KeyspaceStraightSchema(KeyspaceBase):
    wordlist1: str
    rule: str
    type: Literal["keyspacestraight"] = "keyspacestraight"


class KeyspaceCombinatorSchema(KeyspaceBase):
    wordlist1: str
    wordlist2: str
    left: str
    right: str
    type: Literal["keyspacecombinator"] = "keyspacecombinator"


class KeyspaceMaskSchema(KeyspaceBase):
    mask: str
    custom_charsets: List[str]
    type: Literal["keyspacemask"] = "keyspacemask"


class KeyspaceHybridSchema(KeyspaceBase):
    wordlist1: str
    mask: str
    wordlist_mask: bool
    type: Literal["keyspacehybrid"] = "keyspacehybrid"
