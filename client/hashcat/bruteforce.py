import logging

from hashcat.executor_base import HashcatExecutorBase
from hashcat.interface import HashcatInterface
from schemas.hashcat_request import HashcatDiscreteTask

from .filemanager import FileManager

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class HashcatBruteforce(HashcatExecutorBase):
    _bound_task: HashcatDiscreteTask

    def __init__(
        self,
        file_manager: FileManager,
        hashcat: HashcatInterface,
        bound_task: HashcatDiscreteTask,
    ):
        super().__init__(file_manager, hashcat)
        self._hashcat.potfile_disable = True
        self._bound_task = bound_task

    # TODO: reimplement for new discrete tasks
    def error_callback(self, hashcat: HashcatInterface):
        logger.error(
            "Hashcat error (%d): %s",
            self.bound_task.job_id,
            self._hashcat.hashcat_status_get_log(),
        )

        self.bound_task = None

    # TODO: reimplement for new discrete tasks
    def warning_callback(self, hashcat: HashcatInterface):
        logger.warning(
            "Hashcat error (%d): %s",
            self.bound_task.job_id,
            self._hashcat.hashcat_status_get_log(),
        )

    # TODO: reimplement for new discrete tasks
    def cracked_callback(self, hashcat: HashcatInterface):
        logger.info("Hashcat cracked another hash (%d)", self.bound_task.job_id)

    # TODO: reimplement for new discrete tasks
    def finished_callback(self, hashcat: HashcatInterface):
        logger.info("Hashcat finished job (%d)", self.bound_task.job_id)

    # TODO: reimplement for new discrete tasks
    def _reset_execute(self, task: HashcatDiscreteTask):
        self._hashcat.reset()
        self._hashcat.hash = "\n".join(task.hashes)
        self._hashcat.hash_mode = task.hash_type._hashcat_type
        self._hashcat.workload_profile = 1
        self._hashcat.outfile = "/tmp/cracked.txt"
        self._hashcat.username = False
        self._hashcat.quiet = True
        self._hashcat.no_threading = True

    # TODO: reimplement for new discrete tasks
    def execute(self, task: HashcatDiscreteTask) -> bool:
        self._reset_execute(task)

        # TODO: get parameters from task
        self._hashcat.mask = "?l?d?d?l"
        self._hashcat.attack_mode = 3

        self.bound_task = task

        self._hashcat.event_connect(self.error_callback, "EVENT_LOG_ERROR")
        self._hashcat.event_connect(self.warning_callback, "EVENT_LOG_WARNING")
        self._hashcat.event_connect(self.cracked_callback, "EVENT_CRACKER_HASH_CRACKED")
        self._hashcat.event_connect(self.finished_callback, "EVENT_CRACKER_FINISHED")

        rc = self._hashcat._hashcat_session_execute()

        self.bound_task = None

        # TODO: read from outfile and return result

        return rc
