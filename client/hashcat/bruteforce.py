import tempfile
import logging

from pathlib import Path

from hashcat.executor_base import HashcatExecutorBase
from hashcat.interface import HashcatInterface
from schemas import AttackMode, HashcatDiscreteTask, HashCrackedValueMapping

from filemanager import FileManager
from schemas.keyspaces import KeyspaceBase
from visitor.ikeyspace import IKeyspaceVisitor
from visitor.keyspace_hashcat import KeyspaceHashcatConfigurerVisitor

logger = logging.getLogger(__name__)


class HashcatBruteforce(HashcatExecutorBase):
    _results_file: Path
    _hashes: list[str]
    _res_separator: str

    _bound_task: HashcatDiscreteTask
    _bound_keyspace: KeyspaceBase
    _configurer: IKeyspaceVisitor

    def __init__(
        self,
        file_manager: FileManager,
        hashcat: HashcatInterface,
        bound_task: HashcatDiscreteTask,
        bound_keyspace: KeyspaceBase,
        hashes: list[str],
    ):
        super().__init__(file_manager, hashcat)
        self._bound_task = bound_task
        self._bound_keyspace = bound_keyspace
        self._hashes = hashes
        self._configurer = KeyspaceHashcatConfigurerVisitor(hashcat, file_manager)
        self._results_file = Path("/tmp/results.txt")
        self._res_separator = "\t"

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

    def _reset_execute(self, attack_mode: AttackMode, hash_file: Path):
        self._hashcat.reset()

        self._hashcat.hash = str(hash_file)
        self._hashcat.hash_mode = self._bound_task.hash_type.hashcat_type
        self._hashcat.workload_profile = 1
        self._hashcat.outfile = str(self._results_file)
        self._hashcat.separator = self._res_separator
        self._hashcat.username = False
        self._hashcat.quiet = True
        self._hashcat.no_threading = True
        self._hashcat.attack_mode = attack_mode.value

    def read_results(self) -> list[HashCrackedValueMapping]:
        results = []
        if not self._results_file.exists():
            return results

        for x in self._results_file.read_text().splitlines():
            hash, cracked_value = x.split(self._res_separator)
            results.append(
                HashCrackedValueMapping(hash=hash, cracked_value=cracked_value)
            )

        self._results_file.unlink(missing_ok=True)
        return results

    def execute(self) -> int:
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as hash_file:
            hash_file.write("\n".join(self._hashes))
            hash_file.close()
            hash_file_path = Path(hash_file.name)

            self._reset_execute(self._bound_keyspace.attack_mode, hash_file_path)
            self._bound_keyspace.accept(self._configurer)

            self._hashcat.event_connect(self.error_callback, "EVENT_LOG_ERROR")
            self._hashcat.event_connect(self.warning_callback, "EVENT_LOG_WARNING")

            try:
                rc = self._hashcat.hashcat_session_execute()
            except Exception:
                raise
            finally:
                hash_file_path.unlink(missing_ok=True)

            return rc
