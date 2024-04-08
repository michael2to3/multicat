from abc import ABC
from typing import List

from pydantic import BaseModel, Field

from .hashcat_request import HashcatOptions, HashType


class HashcatDiscreteTask(BaseModel, ABC):
    job_id: int
    hash_type: HashType
    hashes: List[str]
    keyspace_skip: int = 0
    keyspace_work: int = 0


class HashcatStep(BaseModel):
    options: HashcatOptions = Field(default_factory=HashcatOptions)
    wordlists: List[str] = Field(default_factory=list)
    rules: List[str] = Field(default_factory=list)
    masks: List[str] = Field(default_factory=list)


class Steps(BaseModel):
    steps: List[HashcatStep] = Field(default_factory=list)
