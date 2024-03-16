from typing import List
from enum import Enum
from pydantic import BaseModel, Field, validator, field_validator


class AttackMode(int, Enum):
    DICTIONARY = 0
    MASK = 3
    HYBRID_WORDLIST_MASK = 6
    HYBRID_MASK_WORDLIST = 7


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
