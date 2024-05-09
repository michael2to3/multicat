from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum, auto
from typing import ClassVar, List

from pydantic import BaseModel, Field, field_validator

from visitor.ihashcatstep import IHashcatStepVisitor

from .hashcat_request import AttackMode, CustomCharset, HashcatOptions, HashType


class HashcatDiscreteTask(BaseModel, ABC):
    job_id: int
    hash_type: HashType
    keyspace_skip: int = 0
    keyspace_work: int = 0


class BaseStep(BaseModel, ABC):
    options: HashcatOptions = Field(default_factory=HashcatOptions)

    @classmethod
    def from_yaml(cls, constructor, node):
        node_data = list(constructor.construct_yaml_map(node))
        return cls(**node_data[0])

    @abstractmethod
    def accept(self, visitor: IHashcatStepVisitor):
        pass


class StraightStep(BaseStep):
    yaml_tag: ClassVar[str] = "!straight"
    attack_mode: AttackMode = AttackMode.DICTIONARY

    wordlists: List[str]
    rules: List[str] = Field(default_factory=list)

    def accept(self, visitor: IHashcatStepVisitor):
        visitor.process_straight(self)


class CombinatorStep(BaseStep):
    yaml_tag: ClassVar[str] = "!combinator"
    attack_mode: AttackMode = AttackMode.COMBINATOR

    left_wordlists: List[str]
    right_wordlists: List[str]
    left_rules: List[str] = Field(default_factory=list)
    right_rules: List[str] = Field(default_factory=list)

    def accept(self, visitor: IHashcatStepVisitor):
        visitor.process_combinator(self)


class MaskStep(BaseStep):
    yaml_tag: ClassVar[str] = "!mask"

    attack_mode: AttackMode = AttackMode.COMBINATOR

    masks: List[str]
    custom_charsets: List[CustomCharset] = Field(default_factory=list)

    def accept(self, visitor: IHashcatStepVisitor):
        visitor.process_mask(self)


class HybridStep(BaseStep):
    yaml_tag: ClassVar[str] = "!hybrid"
    attack_mode: AttackMode

    wordlists: List[str]
    masks: List[str]
    wordlist_mask: bool = True
    custom_charsets: List[CustomCharset] = Field(default_factory=list)
    increment: bool = False

    @field_validator("attack_mode")
    @classmethod
    def change_attack_mode(cls, v, _) -> AttackMode:
        if v is not None:
            return v

        if cls.wordlist_mask:
            return AttackMode.HYBRID_DICT_MASK

        return AttackMode.HYBRID_MASK_DICT

    def accept(self, visitor: IHashcatStepVisitor):
        visitor.process_hybrid(self)


class Steps(BaseModel):
    steps: List[BaseStep] = Field(default_factory=list)


class StepStatus(Enum):
    UNKNOWN = auto()
    SUCCESS = auto()
    FAILED = auto()
    PROCESSING = auto()


class StepsList(BaseModel):
    name: str
    status: StepStatus
    timestamp: datetime
