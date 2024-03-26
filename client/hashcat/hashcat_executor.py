import logging

from typing import Optional
from .hashcat import Hashcat
from .filemanager import FileManager
from schemas import HashcatDiscreteTask, HashcatStep

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

    def calc_keyspace(self, step: HashcatStep) -> Optional[int]:
        self.hashcat.attack_mode = 0
        keyspace = 0

        if self.hashcat.attack_mode == 0:
            for wordlist in step.wordlists:
                self.hashcat.reset()
                self.hashcat.keyspace = True
                self.hashcat.no_threading = True
                self.hashcat.quiet = True
                self.hashcat.attack_mode = 0
                self.hashcat.dict1 = self.file_manager.get_wordlist(wordlist)

                rc = self.hashcat.hashcat_session_execute()
                if rc < 0:
                    return None

                keyspace += self.hashcat.words_base

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
