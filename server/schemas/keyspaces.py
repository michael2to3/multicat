from typing import List, Literal

from pydantic import BaseModel

from schemas.hashcat_request import AttackMode

class KeyspaceBase(BaseModel):
    attack_mode: AttackMode
    value: int

    class Config:
        from_attributes = True
        fields = {"attack_mode": {"exclude": True}}


class KeyspaceStraightSchema(KeyspaceBase):
    attack_mode: AttackMode = AttackMode.DICTIONARY
    wordlist1: str
    rule: str
    type: Literal["keyspacestraight"] = "keyspacestraight"


class KeyspaceCombinatorSchema(KeyspaceBase):
    attack_mode: AttackMode = AttackMode.COMBINATOR
    wordlist1: str
    wordlist2: str
    left: str
    right: str
    type: Literal["keyspacecombinator"] = "keyspacecombinator"


class KeyspaceMaskSchema(KeyspaceBase):
    attack_mode: AttackMode = AttackMode.MASK
    mask: str
    custom_charsets: List[str]
    type: Literal["keyspacemask"] = "keyspacemask"


class KeyspaceHybridSchema(KeyspaceBase):
    wordlist1: str
    mask: str
    wordlist_mask: bool
    type: Literal["keyspacehybrid"] = "keyspacehybrid"

    @property
    def attack_mode(self) -> AttackMode:
        if self.wordlist_mask:
            return AttackMode.HYBRID_WORDLIST_MASK

        return AttackMode.HYBRID_MASK_WORDLIST
