import logging
from typing import Optional

from hashcat.hashcat_executor_base import HashcatExecutorBase
from hashcat.hashcat_interface import HashcatInterface
from schemas.hashcat_request import HashcatDiscreteTask

from .filemanager import FileManager

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class HashcatBruteforce(HashcatExecutorBase):
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
