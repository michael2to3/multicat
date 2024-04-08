from abc import ABC
import logging

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Literal, Union

from hashcat.hashcat_interface import HashcatInterface
from .hashcat import Hashcat
from .filemanager import FileManager
from schemas import AttackMode, CustomCharset, KeyspaceSchema, HashType

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class UnimplementedAttackModeException(Exception):
    pass


class HashcatCalculationException(Exception):
    pass


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

    def calc_keyspace(self, hashcat_executor: "HashcatExecutor") -> Dict:
        return hashcat_executor._calc_keyspace(AttackMode.DICTIONARY, self)

    def configure(self, hashcat: Hashcat, file_manager: FileManager):
        hashcat.dict1 = file_manager.get_wordlist(self.wordlist1)

        if self.rule:
            # It's better to provide one rule at a time, because we can quickly exceed available memory, or reach integer overflow
            hashcat.rules = (file_manager.get_rule(self.rule),)

    def build_keyspace(self, value) -> KeyspaceSchema:
        return KeyspaceSchema(
            attack_mode=AttackMode.DICTIONARY.value,
            wordlist1=self.wordlist1,
            rule=self.rule,
            value=value,
        )


class HashcatDiscreteCombinatorTask(HashcatDiscreteTask):
    wordlist1: str
    wordlist2: str
    left: str = ""
    right: str = ""
    type: Literal["HashcatDiscreteCombinatorTask"] = "HashcatDiscreteCombinatorTask"

    def calc_keyspace(self, hashcat_executor: "HashcatExecutor") -> Dict:
        return hashcat_executor._calc_keyspace(AttackMode.COMBINATOR, self)

    def configure(self, hashcat: Hashcat, file_manager: FileManager):
        hashcat.dict1 = file_manager.get_wordlist(self.wordlist1)
        hashcat.dict2 = file_manager.get_wordlist(self.wordlist2)

        if self.left:
            hashcat.rule_buf_l = file_manager.get_rule(self.left)

        if self.right:
            hashcat.rule_buf_r = file_manager.get_rule(self.right)

    def build_keyspace(self, value) -> KeyspaceSchema:
        return KeyspaceSchema(
            attack_mode=AttackMode.COMBINATOR.value,
            wordlist1=self.wordlist1,
            wordlist2=self.wordlist2,
            left=self.left,
            right=self.right,
            value=value,
        )


class HashcatDiscreteMaskTask(HashcatDiscreteTask):
    mask: str
    custom_charsets: List[CustomCharset] = Field(default_factory=list)
    type: Literal["HashcatDiscreteMaskTask"] = "HashcatDiscreteCombinatorTask"

    def calc_keyspace(self, hashcat_executor: "HashcatExecutor") -> Dict:
        return hashcat_executor._calc_keyspace(AttackMode.MASK, self)

    def configure(self, hashcat: Hashcat, _):
        hashcat.mask = self.mask

        if self.custom_charsets:
            for charset in self.custom_charsets:
                setattr(
                    hashcat,
                    f"custom_charset_{charset.charset_id}",
                    charset.charset,
                )

    def build_keyspace(self, value) -> KeyspaceSchema:
        return KeyspaceSchema(
            attack_mode=AttackMode.MASK.value,
            mask=self.mask,
            custom_charsets="\n".join(
                charset.charset for charset in self.custom_charsets
            ),
            value=value,
        )


class HashcatDiscreteHybridTask(HashcatDiscreteTask):
    wordlist1: str
    mask: str

    wordlist_mask: bool
    type: Literal["HashcatDiscreteHybridTask"] = "HashcatDiscreteHybridTask"

    def calc_keyspace(self, hashcat_executor: "HashcatExecutor") -> Dict:
        if self.wordlist_mask:
            return hashcat_executor._calc_keyspace(
                AttackMode.HYBRID_WORDLIST_MASK, self
            )
        else:
            return hashcat_executor._calc_keyspace(
                AttackMode.HYBRID_MASK_WORDLIST, self
            )

    def configure(self, hashcat: Hashcat, file_manager: FileManager):
        hashcat.dict1 = file_manager.get_wordlist(self.wordlist1)
        hashcat.mask = self.mask

    def build_keyspace(self, value) -> KeyspaceSchema:
        am = AttackMode.HYBRID_WORDLIST_MASK
        if not self.wordlist_mask:
            am = AttackMode.HYBRID_MASK_WORDLIST

        return KeyspaceSchema(
            attack_mode=am.value,
            wordlist1=self.wordlist1,
            mask=self.mask,
            value=value,
        )


class HashcatDiscreteTaskContainer(BaseModel):
    task: Union[HashcatDiscreteTask.get_subclasses()] = Field(discriminator="type")


class HashcatExecutor:
    def __init__(self, file_manager: FileManager, hashcat: HashcatInterface):
        self.file_manager = file_manager

        self.hashcat = hashcat
        self.hashcat.potfile_disable = True
        self.bound_task: Optional[HashcatDiscreteTask] = None

    # TODO: reimplement for new discrete tasks
    def error_callback(self, hInstance):
        logger.error(
            "Hashcat error (%d): %s",
            self.bound_task.job_id,
            self.hashcat.hashcat_status_get_log(),
        )

        self.bound_task = None

    # TODO: reimplement for new discrete tasks
    def warning_callback(self, hInstance):
        logger.warning(
            "Hashcat error (%d): %s",
            self.bound_task.job_id,
            self.hashcat.hashcat_status_get_log(),
        )

    # TODO: reimplement for new discrete tasks
    def cracked_callback(self, hInstance):
        logger.info("Hashcat cracked another hash (%d)", self.bound_task.job_id)

    # TODO: reimplement for new discrete tasks
    def finished_callback(self, hInstance):
        logger.info("Hashcat finished job (%d)", self.bound_task.job_id)

    def _reset_keyspace(self, attack_mode: AttackMode):
        self.hashcat.reset()
        self.hashcat.keyspace = True
        self.hashcat.no_threading = True
        self.hashcat.quiet = True
        self.hashcat.attack_mode = attack_mode.value

    def check_hexec(self) -> bool:
        rc = self.hashcat.hashcat_session_execute()
        if rc < 0:
            logger.error("Hashcat: %s", self.hashcat.hashcat_status_get_log())
            return False

        return True

    def _calc_keyspace(
        self,
        attack_mode: AttackMode,
        task,
    ) -> KeyspaceSchema:
        self._reset_keyspace(attack_mode)
        task.configure(self.hashcat, self.file_manager)

        if not self.check_hexec():
            raise HashcatCalculationException(f"Failed to compute keyspace for {task}")

        return task.build_keyspace(self.hashcat.words_base)

    def devices_info(self) -> Dict:
        self.hashcat.reset()
        self.hashcat.no_threading = True
        self.hashcat.quiet = True
        self.hashcat.backend_info = True

        rc = self.hashcat.hashcat_session_init()

        if rc < 0:
            logger.error("Hashcat: %s", self.hashcat.hashcat_status_get_log())
            raise HashcatCalculationException("Failed to gather devices info")

        return self.hashcat.get_backend_devices_info()

    def _reset_benchmark(self, benchmark_all=False):
        self.hashcat.reset()
        self.hashcat.quiet = True
        self.hashcat.benchmark = True
        self.hashcat.no_threading = True
        self.hashcat.benchmark_all = benchmark_all

    def benchmark(self, hash_modes: List[int]) -> Dict:
        hashrates = {}

        for hash_mode in hash_modes:
            self._reset_benchmark(benchmark_all=False)
            self.hashcat.hash_mode = hash_mode

            if not self.check_hexec():
                raise HashcatCalculationException(
                    f"Failed to benchmark the hash {hash_mode}"
                )

            hashrates[str(hash_mode)] = {
                "overall": self.hashcat.status_get_hashes_msec_all()
            }

        return hashrates

    # TODO: reimplement for new discrete tasks
    def _reset_execute(self, task: HashcatDiscreteTask):
        self.hashcat.reset()
        self.hashcat.hash = "\n".join(task.hashes)
        self.hashcat.hash_mode = task.hash_type.hashcat_type
        self.hashcat.workload_profile = 1
        self.hashcat.outfile = "/tmp/cracked.txt"
        self.hashcat.username = False
        self.hashcat.quiet = True
        self.hashcat.no_threading = True

    # TODO: reimplement for new discrete tasks
    def execute(self, task: HashcatDiscreteTask) -> bool:
        self._reset_execute(task)

        # TODO: get parameters from task
        self.hashcat.mask = "?l?d?d?l"
        self.hashcat.attack_mode = 3

        self.bound_task = task

        self.hashcat.event_connect(self.error_callback, "EVENT_LOG_ERROR")
        self.hashcat.event_connect(self.warning_callback, "EVENT_LOG_WARNING")
        self.hashcat.event_connect(self.cracked_callback, "EVENT_CRACKER_HASH_CRACKED")
        self.hashcat.event_connect(self.finished_callback, "EVENT_CRACKER_FINISHED")

        rc = self.hashcat.hashcat_session_execute()

        self.bound_task = None

        # TODO: read from outfile and return result

        return rc
