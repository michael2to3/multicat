import logging

from filemanager import FileManager
from hashcat import HashcatInterface
from hashcat.attackmode_mapper import AttackModeMapper
from schemas import AttackMode, KeyspaceBase
from visitor.ikeyspace import IKeyspaceVisitor
from visitor.keyspace_hashcat import KeyspaceHashcatConfigurerVisitor

from .executor_base import HashcatExecutorBase

logger = logging.getLogger(__name__)


class HashcatKeyspaceCalculationException(Exception):
    pass


class HashcatKeyspace(HashcatExecutorBase):
    _configurer: IKeyspaceVisitor

    def __init__(self, file_manager: FileManager, hashcat: HashcatInterface):
        super().__init__(file_manager, hashcat)

        self._configurer = KeyspaceHashcatConfigurerVisitor(hashcat, file_manager)

    def _reset_keyspace(self, attack_mode: AttackMode):
        self._hashcat.reset()
        self._hashcat.keyspace = True
        self._hashcat.no_threading = True
        self._hashcat.quiet = True
        self._hashcat.attack_mode = AttackModeMapper.to_int(attack_mode.value)

    def calc_keyspace(
        self,
        task: KeyspaceBase,
    ) -> int:
        self._reset_keyspace(task.attack_mode)
        task.accept(self._configurer)

        if not self.check_hexec():
            raise HashcatKeyspaceCalculationException(
                f"Failed to compute keyspace for {task}"
            )

        return self._hashcat.words_base
