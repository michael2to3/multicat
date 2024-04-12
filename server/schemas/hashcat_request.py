from enum import Enum
from typing import List

from pydantic import AliasChoices, BaseModel, Field, field_validator


class AttackMode(int, Enum):
    DICTIONARY = 0
    COMBINATOR = 1
    MASK = 3
    HYBRID_DICT_MASK = 6
    HYBRID_MASK_DICT = 7


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
    optimization: bool = Field(
        default=False, validation_alias=AliasChoices("optimization", "opt", "O")
    )
    work_mode: int = Field(default=4, validation_alias=AliasChoices("work_mode", "w"))
    dry_run: bool = Field(default=False)
