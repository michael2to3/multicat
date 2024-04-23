import os
import tempfile
import logging
from typing import Dict, List, Tuple

from hashcat.executor_base import HashcatExecutorBase
from hashcat.interface import HashcatInterface
from schemas.hashcat_request import AttackMode, HashcatDiscreteTask

from filemanager import FileManager
from schemas.keyspaces import KeyspaceBase
from visitor.ikeyspace import IKeyspaceVisitor
from visitor.keyspace_hashcat import KeyspaceHashcatConfigurerVisitor

logger = logging.getLogger(__name__)


class HashcatBruteforce(HashcatExecutorBase):
    _results_file: str
    _potfile_path: str
    _hashes: List[str]

    _bound_task: HashcatDiscreteTask
    _bound_keyspace: KeyspaceBase
    _configurer: IKeyspaceVisitor

    def __init__(
        self,
        file_manager: FileManager,
        hashcat: HashcatInterface,
        bound_task: HashcatDiscreteTask,
        bound_keyspace: KeyspaceBase,
        hashes: List[str],
    ):
        super().__init__(file_manager, hashcat)
        self._hashcat.potfile_disable = True
        self._bound_task = bound_task
        self._bound_keyspace = bound_keyspace
        self._hashes = hashes
        self._configurer = KeyspaceHashcatConfigurerVisitor(hashcat, file_manager)
        self._results_file = "/tmp/results.txt"
        self._potfile_path = "/tmp/potfile.txt"

    # TODO: reimplement for new discrete tasks
    def error_callback(self, hashcat: HashcatInterface):
        logger.error(
            "Hashcat error (%d): %s",
            self._bound_task.job_id,
            self._hashcat.hashcat_status_get_log(),
        )

    # TODO: reimplement for new discrete tasks
    def warning_callback(self, hashcat: HashcatInterface):
        logger.warning(
            "Hashcat error (%d): %s",
            self._bound_task.job_id,
            self._hashcat.hashcat_status_get_log(),
        )

    # TODO: reimplement for new discrete tasks
    def cracked_callback(self, hashcat: HashcatInterface):
        logger.info("Hashcat cracked another hash (%d)", self._bound_task.job_id)

    # TODO: reimplement for new discrete tasks
    def finished_callback(self, hashcat: HashcatInterface):
        logger.info("Hashcat finished job (%d)", self._bound_task.job_id)

    # TODO: reimplement for new discrete tasks
    def _reset_execute(self, attack_mode: AttackMode, hash_file: str):
        self._hashcat.reset()

        self._hashcat.hash = hash_file
        self._hashcat.hash_mode = self._bound_task.hash_type.hashcat_type
        self._hashcat.workload_profile = 1
        self._hashcat.outfile = self._results_file
        self._hashcat.separator = "\t"
        self._hashcat.username = False
        self._hashcat.quiet = True
        self._hashcat.no_threading = True
        self._hashcat.attack_mode = attack_mode.value
        self._hashcat.potfile_path = self._potfile_path

    def _init_hashfile(self) -> str:
        hash_file = tempfile.NamedTemporaryFile(mode="w+", delete=False)
        hash_file.write("\n".join(self._hashes))
        hash_file.close()
        return hash_file.name

    def _clear_potfile(self):
        open(self._potfile_path, "w").close()

    def _read_results(self) -> Dict[str, str]:
        results = {}
        try:
            with open(self._results_file, "r") as rf:
                for x in rf.read().splitlines():
                    hash, value = x.split("\t")
                    results[hash] = value

            os.unlink(self._results_file)
        except Exception:
            pass

        self._clear_potfile()
        return results

    # TODO: reimplement for new discrete tasks
    def execute(self) -> Tuple[bool, List]:
        hash_file_name = self._init_hashfile()
        self._reset_execute(self._bound_keyspace.attack_mode, hash_file_name)
        self._bound_keyspace.accept(self._configurer)

        self._hashcat.event_connect(self.error_callback, "EVENT_LOG_ERROR")
        self._hashcat.event_connect(self.warning_callback, "EVENT_LOG_WARNING")
        # self._hashcat.event_connect(self.cracked_callback, "EVENT_CRACKER_HASH_CRACKED")
        # self._hashcat.event_connect(self.finished_callback, "EVENT_CRACKER_FINISHED")

        rc = self._hashcat.hashcat_session_execute()
        os.unlink(hash_file_name)

        results = self._read_results()
        return rc, results
