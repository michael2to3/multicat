from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, parse_obj_as


class AttackMode(str, Enum):
    DICTIONARY = "0"
    MASK = "3"
    HYBRID_WORDLIST_MASK = "6"
    HYBRID_MASK_WORDLIST = "7"


class CustomCharset(BaseModel):
    charset_id: str
    charset: str

    @field_validator("charset_id")
    @classmethod
    def check_charset_id_valid(cls, v):
        if v not in range(1, 5):
            raise ValueError("charset_id must be between 1 and 4")
        return v

    def to_hashcat_format(self):
        return f"-{self.charset_id}", self.charset


class HashcatOptions(BaseModel):
    optimization: bool = Field(default=False, alias="O")
    work_mode: int = Field(alias="w")
    increment: bool = Field(default=False, alias="increment")
    custom_charsets: List[CustomCharset] = Field(default_factory=list)


class BaseStep(BaseModel):
    options: Optional[HashcatOptions] = None


class HashcatStep(BaseModel):
    wordlists: Optional[List[str]] = None
    rules: Optional[List[str]] = None
    masks: Optional[List[str]] = None


class Steps(BaseModel):
    steps: List[BaseStep] = Field(default_factory=list)


def hashcat_step_constructor(loader, node):
    value = loader.construct_mapping(node, deep=True)
    return parse_obj_as(HashcatStep, value)


class KeyspaceSchema(BaseModel):
    attack_mode: int
    wordlist1: str = ""
    wordlist2: str = "" 
    rule: str = "" 
    left: str = ""
    right: str = ""
    mask: str = ""
    custom_charsets: str = ""
    value: int
