from abc import ABC
from enum import Enum
from typing import List, Optional, Literal, Union

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
    job_id: int = -1
    hash_type: HashType
    hashes: List[str]
    keyspace_skip: int = 0
    keyspace_work: int = 0
    type: Literal['HashcatDiscreteTask']

    @classmethod
    def get_subclasses(cls):
        return tuple(cls.__subclasses__())


class HashcatDiscreteStraightTask(HashcatDiscreteTask):
    wordlist: str
    rule: Optional[str] = None
    type: Literal['HashcatDiscreteStraightTask'] = "HashcatDiscreteStraightTask"

    def get_keyspace_name(self):
        if self.rule:
            return f"wr:{self.dict1}:{self.rule}"

        return f"w:{self.wordlist}"


class HashcatDiscreteCombinatorTask(HashcatDiscreteTask):
    wordlist1: str
    wordlist2: str
    type: Literal['HashcatDiscreteCombinatorTask'] = "HashcatDiscreteCombinatorTask"

    def get_keyspace_name(self):
        return f"ww:{self.wordlist1}:{self.wordlist2}"


class HashcatDiscreteMaskTask(HashcatDiscreteTask):
    mask: str
    custom_charsets: List[CustomCharset] = Field(default_factory=list)
    type: Literal['HashcatDiscreteMaskTask'] = "HashcatDiscreteCombinatorTask"

    def get_keyspace_name(self):
        if len(self.custom_charsets):
            charsets = ":".join(charset.charset for charset in self.custom_charsets)
            return f"mc:{self.mask}:{charsets}"

        return f"m:{self.mask}"

class HashcatDiscreteHybridTask(HashcatDiscreteTask):
    wordlist: str
    mask: str

    wordlist_mask: bool
    type: Literal['HashcatDiscreteHybridTask'] = "HashcatDiscreteHybridTask"

    def get_keyspace_name(self):
        return f"wm:{self.wordlist}:{self.mask}"


class HashcatDiscreteTaskContainer(BaseModel):
    task: Union[HashcatDiscreteTask.get_subclasses()] = Field(discriminator="type")


class HashcatStep(BaseModel):
    options: HashcatOptions = Field(default_factory=HashcatOptions)
    wordlists: List[str] = Field(default_factory=list)
    rules: List[str] = Field(default_factory=list)
    masks: List[str] = Field(default_factory=list)

    def yield_discrete_tasks(self):
        # TODO: remove fixed calculation
        self.options.attack_mode = AttackMode.DICTIONARY

        match self.options.attack_mode:
            case AttackMode.DICTIONARY:
                if len(self.rules) == 0:
                    for wordlist in self.wordlists:
                        yield HashcatDiscreteStraightTask(
                            job_id = -1,
                            hash_type = HashType(hashcat_type=-1, human_readable="unnamed"),
                            hashes = list(),
                            wordlist = wordlist,
                        )
                else:
                    for wordlist in self.wordlists:
                        for rule in self.rules:
                            yield HashcatDiscreteStraightTask(
                                job_id = -1,
                                hash_type = HashType(hashcat_type=-1, human_readable="unnamed"),
                                hashes = list(),
                                wordlist = wordlist,
                                rule = rule,
                            )

            case _:
                raise NotImplementedError("Not implemented")


class Steps(BaseModel):
    steps: List[HashcatStep] = Field(default_factory=list)

    def yield_discrete_tasks(self):
        for step in self.steps:
            for task in step.yield_discrete_tasks():
                yield task
