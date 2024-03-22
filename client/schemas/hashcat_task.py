from typing import List

from pydantic import BaseModel

from .hashcat_request import HashcatStep, HashType


class HashcatDiscreteTask(BaseModel):
    job_id: int
    hash_type: HashType
    step: HashcatStep
    hashes: List[str]
