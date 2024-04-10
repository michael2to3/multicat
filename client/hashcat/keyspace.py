import logging
from abc import ABC, abstractmethod
from typing import List, Literal, Tuple, Union

from pydantic import BaseModel, Field

from hashcat.interface import HashcatInterface
from schemas import AttackMode, KeyspaceSchema

from .executor_base import HashcatExecutorBase
from .filemanager import FileManager
from .hashcat import Hashcat

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class HashcatKeyspaceCalculationException(Exception):
    pass


class KeyspaceBase(BaseModel, ABC):
    attack_mode: AttackMode
    value: int

    @classmethod
    def get_subclasses(cls) -> Tuple:
        return tuple(cls.__subclasses__())

    class Config:
        from_attributes = True
        fields = {"attack_mode": {"exclude": True}}

    @abstractmethod
    def configure(self, hashcat: Hashcat, file_manager: FileManager):
        pass


class KeyspaceStraightSchema(KeyspaceBase):
    attack_mode: AttackMode = AttackMode.DICTIONARY
    wordlist1: str
    rule: str
    type: Literal["keyspacestraight"] = "keyspacestraight"

    def configure(self, hashcat: Hashcat, file_manager: FileManager):
        hashcat.dict1 = file_manager.get_wordlist(self.wordlist1)

        if self.rule:
            # It's better to provide one rule at a time, because we can quickly exceed available memory, or reach integer overflow
            hashcat.rules = (file_manager.get_rule(self.rule),)


class KeyspaceCombinatorSchema(KeyspaceBase):
    attack_mode: AttackMode = AttackMode.COMBINATOR
    wordlist1: str
    wordlist2: str
    left: str
    right: str
    type: Literal["keyspacecombinator"] = "keyspacecombinator"

    def configure(self, hashcat: Hashcat, file_manager: FileManager):
        hashcat.dict1 = file_manager.get_wordlist(self.wordlist1)
        hashcat.dict2 = file_manager.get_wordlist(self.wordlist2)

        if self.left:
            hashcat.rule_buf_l = file_manager.get_rule(self.left)

        if self.right:
            hashcat.rule_buf_r = file_manager.get_rule(self.right)


class KeyspaceMaskSchema(KeyspaceBase):
    attack_mode: AttackMode = AttackMode.MASK
    mask: str
    custom_charsets: List[str]
    type: Literal["keyspacemask"] = "keyspacemask"

    def configure(self, hashcat: Hashcat, _):
        hashcat.mask = self.mask

        if self.custom_charsets:
            for charset in self.custom_charsets:
                setattr(
                    hashcat,
                    f"custom_charset_{charset.charset_id}",
                    charset.charset,
                )


class KeyspaceHybridSchema(KeyspaceBase):
    wordlist1: str
    mask: str
    wordlist_mask: bool
    type: Literal["keyspacehybrid"] = "keyspacehybrid"

    @property
    def attack_mode(self) -> AttackMode:
        if self.wordlist_mask:
            return AttackMode.HYBRID_WORDLIST_MASK

        return AttackMode.HYBRID_MASK_WORDLIST

    def configure(self, hashcat: Hashcat, file_manager: FileManager):
        hashcat.dict1 = file_manager.get_wordlist(self.wordlist1)
        hashcat.mask = self.mask


class KeyspaceTaskContainer(BaseModel):
    task: Union[KeyspaceBase.get_subclasses()] = Field(discriminator="type")


class HashcatKeyspace(HashcatExecutorBase):
    def __init__(self, file_manager: FileManager, hashcat: HashcatInterface):
        self.file_manager = file_manager
        self.hashcat = hashcat

    def _reset_keyspace(self, attack_mode: AttackMode):
        self.hashcat.reset()
        self.hashcat.keyspace = True
        self.hashcat.no_threading = True
        self.hashcat.quiet = True
        self.hashcat.attack_mode = attack_mode.value

    def calc_keyspace(
        self,
        task,
    ) -> KeyspaceSchema:
        task = KeyspaceTaskContainer.model_validate({"task": task})
        task: KeyspaceBase = task.task

        self._reset_keyspace(task.attack_mode)
        task.configure(self.hashcat, self.file_manager)

        if not self.check_hexec():
            raise HashcatKeyspaceCalculationException(
                f"Failed to compute keyspace for {task}"
            )

        return self.hashcat.words_base
