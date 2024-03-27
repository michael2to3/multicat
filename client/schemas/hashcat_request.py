from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, validator


class AttackMode(int, Enum):
    DICTIONARY = 0
    COMBINATOR = 1
    MASK = 3
    HYBRID_WORDLIST_MASK = 6
    HYBRID_MASK_WORDLIST = 7


class HashType(BaseModel):
    hashcat_type: int
    human_readable: str


class CustomCharset(BaseModel):
    charset_id: int
    charset: str

    @field_validator("charset_id")
    @classmethod
    def check_charset_id_valid(cls, v):
        if v not in range(1, 5):
            raise ValueError("charset_id must be between 1 and 4")
        return v


class HashcatOptions(BaseModel):
    optimization: bool = Field(default=False, alias="O")
    work_mode: int = Field(default=4, alias="w")
    increment: bool = Field(default=False, alias="increment")
    custom_charsets: List[CustomCharset] = Field(default_factory=list)
    attack_mode: AttackMode = Field(default=None, alias="a")
    dry_run: bool = Field(default=False)

    @validator("attack_mode", pre=True, always=True)
    @classmethod
    def set_default_attack_mode(cls, v, values):
        if v is not None:
            return v

        rules = values.get("rules", [])
        if rules:
            return AttackMode.HYBRID_MASK_WORDLIST
        return AttackMode.MASK


class HashcatStep(BaseModel):
    options: HashcatOptions = Field(default_factory=HashcatOptions)
    wordlists: List[str] = Field(default_factory=list)
    rules: List[str] = Field(default_factory=list)
    masks: List[str] = Field(default_factory=list)


class Steps(BaseModel):
    steps: List[HashcatStep] = Field(default_factory=list)


class Keyspace(BaseModel):
    dict1: Optional[str] = None
    dict2: Optional[str] = None
    rule: Optional[str] = None
    mask: Optional[str] = None
    charsets: Optional[str] = None
    attack_mode: AttackMode
    value: int

    @property
    def name(self):
        match self.attack_mode:
            case AttackMode.DICTIONARY:
                if self.rule:
                    return f"wr:{self.dict1}:{self.rule}"

                return f"w:{self.dict1}"

            case AttackMode.COMBINATOR:
                return f"ww:{self.dict1}:{self.dict2}"

            case AttackMode.MASK:
                if self.charsets:
                    return f"mc:{self.mask}:{self.charsets}"

                return f"m:{self.mask}"

            case AttackMode.HYBRID_WORDLIST_MASK | AttackMode.HYBRID_MASK_WORDLIST:
                return f"wm:{self.dict1}:{self.mask}"
