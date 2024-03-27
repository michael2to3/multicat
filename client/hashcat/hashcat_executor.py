import logging

from typing import Optional, List
from .hashcat import Hashcat
from .filemanager import FileManager
from schemas import HashcatDiscreteTask, HashcatStep, AttackMode, CustomCharset

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class HashcatExecutor:
    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager

        self.hashcat = Hashcat()
        self.hashcat.potfile_disable = True
        self.busy = False
        self.bound_task: Optional[HashcatDiscreteTask] = None

    def error_callback(self, hInstance):
        logger.error(
            "Hashcat error ({}): {}".format(
                self.bound_task.job_id, self.hashcat.hashcat_status_get_log()
            )
        )
        self.busy = False
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
        self.busy = False
        self.bound_task = None

    def reset_keyspace(self, attack_mode: AttackMode):
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
        self.reset_keyspace(attack_mode)

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

    def calc_keyspace(self, step: HashcatStep) -> Optional[int]:
        attack_mode = step.options.attack_mode
        keyspace = 0

        match attack_mode:
            case AttackMode.DICTIONARY:
                if len(step.rules) == 0:
                    for wordlist in step.wordlists:
                        keyspace += self._calc_keyspace(attack_mode, dict1=wordlist)
                else:
                    for wordlist in step.wordlists:
                        for rule in step.rules:
                            keyspace += self._calc_keyspace(
                                attack_mode, dict1=wordlist, rule=rule
                            )

            case AttackMode.COMBINATOR:
                for wordlist in step.wordlists:
                    # TODO: Implement left/right rules
                    dict1, dict2 = wordlist.split(" ")
                    keyspace += self._calc_keyspace(
                        attack_mode, dict1=dict1, dict2=dict2
                    )

            case AttackMode.MASK:
                for mask in step.masks:
                    keyspace += self._calc_keyspace(
                        attack_mode, mask=mask, custom_charsets=step.custom_charsets
                    )

            case AttackMode.HYBRID_WORDLIST_MASK | AttackMode.HYBRID_MASK_WORDLIST:
                for wordlist in step.wordlists:
                    for mask in step.masks:
                        keyspace += self._calc_keyspace(
                            attack_mode, dict1=wordlist, mask=mask
                        )

        return keyspace

    def execute(self, task: HashcatDiscreteTask) -> bool:
        if self.busy:
            return False

        self.hashcat.hash = "\n".join(task.hashes)
        self.hashcat.hash_mode = task.hash_type.hashcat_type
        self.hashcat.workload_profile = 1
        self.hashcat.outfile = "/tmp/cracked.txt"
        self.hashcat.username = False
        self.hashcat.quiet = True

        # TODO: get parameters from task
        self.hashcat.mask = "?l?d?d?l"
        self.hashcat.attack_mode = 3

        self.hashcat.event_connect(self.error_callback, "EVENT_LOG_ERROR")
        self.hashcat.event_connect(self.warning_callback, "EVENT_LOG_WARNING")
        self.hashcat.event_connect(self.cracked_callback, "EVENT_CRACKER_HASH_CRACKED")
        self.hashcat.event_connect(self.finished_callback, "EVENT_CRACKER_FINISHED")

        rc = self.hashcat.hashcat_session_execute() >= 0
        if rc:
            self.busy = True
            self.bound_task = task

        return rc
