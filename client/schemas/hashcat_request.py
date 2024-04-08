from abc import ABC
from enum import Enum
from typing import List, Literal, Union

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


class HashcatDiscreteTask(BaseModel, ABC):
    job_id: int
    hash_type: HashType
    hashes: List[str]
    keyspace_skip: int = 0
    keyspace_work: int = 0
    type: Literal["HashcatDiscreteTask"]

    @classmethod
    def get_subclasses(cls):
        return tuple(cls.__subclasses__())


class HashcatDiscreteStraightTask(HashcatDiscreteTask):
    wordlist1: str
    rule: str = ""
    type: Literal["HashcatDiscreteStraightTask"] = "HashcatDiscreteStraightTask"


class HashcatDiscreteCombinatorTask(HashcatDiscreteTask):
    wordlist1: str
    wordlist2: str
    left: str = ""
    right: str = ""
    type: Literal["HashcatDiscreteCombinatorTask"] = "HashcatDiscreteCombinatorTask"


class HashcatDiscreteMaskTask(HashcatDiscreteTask):
    mask: str
    custom_charsets: List[CustomCharset] = Field(default_factory=list)
    type: Literal["HashcatDiscreteMaskTask"] = "HashcatDiscreteCombinatorTask"


class HashcatDiscreteHybridTask(HashcatDiscreteTask):
    wordlist1: str
    mask: str

    wordlist_mask: bool
    type: Literal["HashcatDiscreteHybridTask"] = "HashcatDiscreteHybridTask"


class HashcatDiscreteTaskContainer(BaseModel):
    task: Union[
        HashcatDiscreteTask.get_subclasses()
    ] = Field(discriminator="type")


class HashcatStep(BaseModel):
    options: HashcatOptions = Field(default_factory=HashcatOptions)
    wordlists: List[str] = Field(default_factory=list)
    rules: List[str] = Field(default_factory=list)
    masks: List[str] = Field(default_factory=list)


class Steps(BaseModel):
    steps: List[HashcatStep] = Field(default_factory=list)


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
