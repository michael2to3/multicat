import logging

from hashcat.configurer import IHashcatConfigurer
from schemas import AttackMode, KeyspaceBase

from .executor_base import HashcatExecutorBase

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class HashcatKeyspaceCalculationException(Exception):
    pass


class HashcatKeyspace(HashcatExecutorBase):
    def _reset_keyspace(self, attack_mode: AttackMode):
        self._hashcat.reset()
        self._hashcat.keyspace = True
        self._hashcat.no_threading = True
        self._hashcat.quiet = True
        self._hashcat.attack_mode = attack_mode.value

    def calc_keyspace(
        self,
        task: KeyspaceBase,
        configure: IHashcatConfigurer
    ) -> int:
        self._reset_keyspace(task.attack_mode)
        task.accept(configure)

        if not self.check_hexec():
            raise HashcatKeyspaceCalculationException(
                f"Failed to compute keyspace for {task}"
            )

        return self._hashcat.words_base
