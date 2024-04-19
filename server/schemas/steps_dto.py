from datetime import datetime
from enum import Enum, auto

from pydantic import BaseModel


class StepStatus(Enum):
    UNKNOWN = auto()
    SUCCESS = auto()
    FAILED = auto()
    PROCESSING = auto()


class StepsList(BaseModel):
    name: str
    status: StepStatus
    timestamp: datetime
