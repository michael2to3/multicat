import logging

from pydantic import InstanceOf
from typing import Optional, List, Tuple, Dict

from config import Config
from schemas.hashcat_request import HashcatDiscreteCombinatorTask, HashcatDiscreteHybridTask, HashcatDiscreteMaskTask
from .hashcat import Hashcat
from .filemanager import FileManager
from schemas import HashcatDiscreteTask, HashcatDiscreteStraightTask, HashcatStep, AttackMode, CustomCharset

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class HashcatExecutor(metaclass=Singleton):
    def __init__(self):
        self.file_manager = FileManager(Config.get("RULES_DIR"), Config.get("WORDLISTS_DIR"))

        self.hashcat = Hashcat()
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
            logger.error("Hashcat: ", self.hashcat.hashcat_status_get_log())
            return False

        return True

    def _calc_keyspace(
        self,
        attack_mode: AttackMode,
        dict1: Optional[str] = None,
        dict2: Optional[str] = None,
        rule: Optional[str] = None,
        mask: Optional[str] = None,
        left: Optional[str] = None, # Left rule
        right: Optional[str] = None, # Right rule
        custom_charsets: Optional[List[CustomCharset]] = None,
    ) -> Optional[int]:
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

        if custom_charsets and len(custom_charsets):
            for charset in custom_charsets:
                setattr(
                    self.hashcat,
                    f"custom_charset_{charset.charset_id}",
                    charset.charset,
                )

        if not self.check_hexec():
            return None

        return self.hashcat.words_base

    def calc_keyspace(self, task: InstanceOf[HashcatDiscreteTask]) -> Tuple[str, Optional[int]]:
        value = 0

        if isinstance(task, HashcatDiscreteStraightTask):
            value = self._calc_keyspace(AttackMode.DICTIONARY, dict1=task.wordlist, rule=task.rule)
        elif isinstance(task, HashcatDiscreteCombinatorTask):
            value = self._calc_keyspace(AttackMode.COMBINATOR, dict1=task.wordlist1, dict2=task.wordlist2, left=task.left, right=task.right)
        elif isinstance(task, HashcatDiscreteMaskTask):
            value = self._calc_keyspace(AttackMode.MASK, mask=task.mask, custom_charsets=task.custom_charsets)
        elif isinstance(task, HashcatDiscreteHybridTask):
            if task.wordlist_mask:
                value = self._calc_keyspace(AttackMode.HYBRID_WORDLIST_MASK, dict1=task.wordlist, mask=task.mask)
            else:
                value = self._calc_keyspace(AttackMode.HYBRID_MASK_WORDLIST, dict1=task.wordlist, mask=task.mask)
        else:
            raise Exception("Unimplemented")

        return (task.get_keyspace_name(), value)

    def devices_info(self) -> Optional[Dict]:
        self.hashcat.reset()
        self.hashcat.no_threading = True
        self.hashcat.quiet = True
        self.hashcat.backend_info = True

        rc = self.hashcat.hashcat_session_init()

        if rc < 0:
            logger.error("Hashcat: ", self.hashcat.hashcat_status_get_log())
            return None

        return self.hashcat.get_backend_devices_info()

    def _reset_benchmark(self, benchmark_all=False):
        self.hashcat.reset()
        self.hashcat.quiet = True
        self.hashcat.benchmark = True
        self.hashcat.no_threading = True
        self.hashcat.benchmark_all = benchmark_all

    def benchmark(self, hash_modes: Optional[List[int]] = None):
        hashrates = {}
        def set_hashrate():
            hashrates[str(self.hashcat.hash_mode)] = {
                "overall": self.hashcat.status_get_hashes_msec_all()
            }

        if hash_modes and len(hash_modes):
            for hash_mode in hash_modes:
                self._reset_benchmark(benchmark_all=False)
                self.hashcat.hash_mode = hash_mode

                if not self.check_hexec():
                    return None

                set_hashrate()
        else:
            self._reset_benchmark(benchmark_all=True)
            self.hashcat.event_connect(set_hashrate, "EVENT_CRACKER_FINISHED")

            if not self.check_hexec():
                return None

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
