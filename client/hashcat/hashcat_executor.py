import logging

from pydantic import InstanceOf, BaseModel, Field
from typing import Optional, List, Tuple, Dict, Literal, Union

from config import Config, Singleton
from hashcat.hashcat_interface import HashcatInterface
from .hashcat import Hashcat
from .filemanager import FileManager
from schemas import HashcatDiscreteTask, HashcatStep, AttackMode, CustomCharset

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class UnimplementedAttackModeException(Exception):
    pass


class HashcatCalculationException(Exception):
    pass


class HashcatDiscreteStraightTask(HashcatDiscreteTask):
    wordlist1: str
    rule: str = ""
    type: Literal["HashcatDiscreteStraightTask"] = "HashcatDiscreteStraightTask"

    def calc_keyspace(self, hashcat_executor: 'HashcatExecutor') -> Dict:
        return hashcat_executor._calc_keyspace(AttackMode.DICTIONARY, dict1=self.wordlist1, rule=self.rule)


class HashcatDiscreteCombinatorTask(HashcatDiscreteTask):
    wordlist1: str
    wordlist2: str
    # Left/right rules
    left: str = ""
    right: str = ""
    type: Literal["HashcatDiscreteCombinatorTask"] = "HashcatDiscreteCombinatorTask"

    def calc_keyspace(self, hashcat_executor: 'HashcatExecutor') -> Dict:
        return hashcat_executor._calc_keyspace(AttackMode.COMBINATOR, dict1=self.wordlist1, dict2=self.wordlist2, left=self.left, right=self.right)



class HashcatDiscreteMaskTask(HashcatDiscreteTask):
    mask: str
    custom_charsets: List[CustomCharset] = Field(default_factory=list)
    type: Literal["HashcatDiscreteMaskTask"] = "HashcatDiscreteCombinatorTask"

    def calc_keyspace(self, hashcat_executor: 'HashcatExecutor') -> Dict:
        return hashcat_executor._calc_keyspace(AttackMode.MASK, mask=self.mask, custom_charsets=self.custom_charsets)


class HashcatDiscreteHybridTask(HashcatDiscreteTask):
    wordlist1: str
    mask: str

    wordlist_mask: bool
    type: Literal["HashcatDiscreteHybridTask"] = "HashcatDiscreteHybridTask"

    def calc_keyspace(self, hashcat_executor: 'HashcatExecutor') -> Dict:
        if self.wordlist_mask:
            return hashcat_executor._calc_keyspace(AttackMode.HYBRID_WORDLIST_MASK, dict1=self.wordlist1, mask=self.mask)
        else:
            return hashcat_executor._calc_keyspace(AttackMode.HYBRID_MASK_WORDLIST, dict1=self.wordlist1, mask=self.mask)


class HashcatDiscreteTaskContainer(BaseModel):
    task: Union[HashcatDiscreteStraightTask, HashcatDiscreteCombinatorTask, HashcatDiscreteMaskTask, HashcatDiscreteHybridTask] = Field(discriminator="type")


class HashcatExecutor(metaclass=Singleton):
    def __init__(self, file_manager: FileManager, hashcat: HashcatInterface):
        self.file_manager = file_manager

        self.hashcat = hashcat
        self.hashcat.potfile_disable = True
        self.bound_task: Optional[InstanceOf[HashcatDiscreteTask]] = None

    # TODO: reimplement for new discrete tasks
    def error_callback(self, hInstance):
        logger.error(
            "Hashcat error (%d): %s",
            self.bound_task.job_id, self.hashcat.hashcat_status_get_log()
        )

        self.bound_task = None

    # TODO: reimplement for new discrete tasks
    def warning_callback(self, hInstance):
        logger.warning(
            "Hashcat error (%d): %s",
            self.bound_task.job_id, self.hashcat.hashcat_status_get_log()
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
        dict1: str = "",
        dict2: str = "",
        rule: str = "",
        mask: str = "",
        left: str = "", # Left rule
        right: str = "", # Right rule
        custom_charsets: Optional[List[CustomCharset]] = None,
    ) -> Dict:
        self._reset_keyspace(attack_mode)

        if dict1:
            self.hashcat.dict1 = self.file_manager.get_wordlist(dict1)

        if dict2:
            self.hashcat.dict2 = self.file_manager.get_wordlist(dict2)

        if rule:
            # It's better to provide one rule at a time, because we can quickly exceed available memory, or reach integer overflow
            self.hashcat.rules = (self.file_manager.get_rule(rule),)

        if left:
            self.hashcat.rule_buf_l = left

        if right:
            self.hashcat.rule_buf_r = right

        if mask:
            self.hashcat.mask = mask

        if custom_charsets:
            for charset in custom_charsets:
                setattr(
                    self.hashcat,
                    f"custom_charset_{charset.charset_id}",
                    charset.charset,
                )

        if not self.check_hexec():
            raise HashcatCalculationException(f"Failed to compute keyspace for {dict1} {dict2} {rule} {mask} {left} {right} {custom_charsets}")

        return {
            "attack_mode": attack_mode.value,
            "wordlist1": dict1,
            "wordlist2": dict2,
            "rule": rule,
            "left": left,
            "right": right,
            "mask": mask,
            "custom_charsets": custom_charsets,
            "value": self.hashcat.words_base
        }

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
                raise HashcatCalculationException(f"Failed to benchmark the hash {hash_mode}")

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
