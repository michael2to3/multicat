import logging

from pydantic import InstanceOf
from typing import Optional, List, Tuple, Dict

from config import Config
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
        self.bound_task: Optional[HashcatDiscreteTask] = None

    def error_callback(self, hInstance):
        logger.error(
            "Hashcat error ({}): {}".format(
                self.bound_task.job_id, self.hashcat.hashcat_status_get_log()
            )
        )
        self.bound_task = None

    def warning_callback(self, hInstance):
        logger.warning(
            "Hashcat warning ({}): {}".format(
                self.bound_task.job_id, self.hashcat.hashcat_status_get_log()
            )
        )

    def cracked_callback(self, hInstance):
        logger.info(f"Hashcat cracked another hash ({self.bound_task.job_id})")

    def finished_callback(self, hInstance):
        logger.info(f"Hashcat finished job ({self.bound_task.job_id})")

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
        custom_charsets: Optional[List[CustomCharset]] = None,
    ) -> Optional[int]:
        self._reset_keyspace(attack_mode)

        if dict1:
            self.hashcat.dict1 = self.file_manager.get_wordlist(dict1)

        if dict2:
            self.hashcat.dict2 = self.file_manager.get_wordlist(dict2)

        if rule:
            self.hashcat.rule = self.file_manager.get_rule(rule)

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

    def calc_keyspace(self, task: InstanceOf[HashcatDiscreteTask]) -> Tuple[str, int]:
        value = 0

        if isinstance(task, HashcatDiscreteStraightTask):
            value = self._calc_keyspace(AttackMode.DICTIONARY, dict1=task.wordlist, rule=task.rule)
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

    def calc_keyspaces(self, step: HashcatStep) -> Optional[int]:
        attack_mode = step.options.attack_mode
        keyspaces = {}
        attack_mode = AttackMode.DICTIONARY

        match attack_mode:
            case AttackMode.DICTIONARY:
                if len(step.rules) == 0:
                    for wordlist in step.wordlists:
                        keyspace = self._calc_keyspace(attack_mode, dict1=wordlist)
                        keyspaces[keyspace.name] = keyspace
                else:
                    for wordlist in step.wordlists:
                        for rule in step.rules:
                            keyspace = self._calc_keyspace(
                                attack_mode, dict1=wordlist, rule=rule
                            )
                            keyspaces[keyspace.name] = keyspace

            case AttackMode.COMBINATOR:
                for wordlist in step.wordlists:
                    # TODO: Implement left/right rules
                    dict1, dict2 = wordlist.split(" ")
                    keyspace = self._calc_keyspace(
                        attack_mode, dict1=dict1, dict2=dict2
                    )
                    keyspaces[keyspace.name] = keyspace

            case AttackMode.MASK:
                for mask in step.masks:
                    keyspace = self._calc_keyspace(
                        attack_mode, mask=mask, custom_charsets=step.custom_charsets
                    )
                    keyspaces[keyspace.name] = keyspace

            case AttackMode.HYBRID_WORDLIST_MASK | AttackMode.HYBRID_MASK_WORDLIST:
                for wordlist in step.wordlists:
                    for mask in step.masks:
                        keyspace = self._calc_keyspace(
                            attack_mode, dict1=wordlist, mask=mask
                        )
                        keyspaces[keyspace.name] = keyspace

        return keyspaces

    def _reset_benchmark(self, benchmark_all=False):
        self.hashcat.reset()
        self.hashcat.quiet = True
        self.hashcat.benchmark = True
        self.hashcat.no_threading = True
        self.hashcat.benchmark_all = benchmark_all

    def benchmark(self, hash_modes: List[int] = None):
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

    def _reset_execute(self, task: HashcatDiscreteTask):
        self.hashcat.reset()
        self.hashcat.hash = "\n".join(task.hashes)
        self.hashcat.hash_mode = task.hash_type.hashcat_type
        self.hashcat.workload_profile = 1
        self.hashcat.outfile = "/tmp/cracked.txt"
        self.hashcat.username = False
        self.hashcat.quiet = True
        self.hashcat.no_threading = True

    def execute(self, task: HashcatDiscreteTask) -> bool:
        self._reset_execute()

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
