from pydantic import BaseModel, field_validator, ConfigDict
from typing import List, Optional
from enum import Enum


class HashcatMode(Enum):
    STRAIGHT = (0, True, False)
    COMBINATION = (1, True, True)
    BRUTE_FORCE = (3, False, True)
    HYBRID_WORDLIST_MASK = (6, True, True)
    HYBRID_MASK_WORDLIST = (7, True, True)
    ASSOCIATION = (9, True, False)

    def __init__(self, mode_num: int, requires_wordlist: bool, requires_mask: bool):
        self.mode_num = mode_num
        self.requires_wordlist = requires_wordlist
        self.requires_mask = requires_mask


class Request(BaseModel):
    hashes: List[str]
    mode: HashcatMode
    wordlists: Optional[List[str]] = None
    masks: Optional[List[str]] = None
    rules_files: Optional[List[str]] = None

    @classmethod
    @field_validator("mode")
    def check_requirements(cls, mode, values):
        if mode.requires_wordlist and not values.get("wordlists"):
            raise ValueError(f"{mode.name} mode requires 'wordlists' to be specified")
        if mode.requires_mask and not values.get("masks"):
            raise ValueError(f"{mode.name} mode requires 'masks' to be specified")
        return mode

    class Config(ConfigDict):
        use_enum_values = True
