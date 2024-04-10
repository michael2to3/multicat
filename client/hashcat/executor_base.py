import logging

from hashcat.filemanager import FileManager
from hashcat.interface import HashcatInterface

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class HashcatExecutorBase:
    _file_manager: FileManager
    _hashcat: HashcatInterface

    def __init__(self, file_manager: FileManager, hashcat: HashcatInterface):
        self._file_manager = file_manager
        self._hashcat = hashcat

    def check_hexec(self) -> bool:
        rc = self._hashcat.hashcat_session_execute()
        if rc < 0:
            logger.error("Hashcat: %s", self._hashcat.hashcat_status_get_log())
            return False

        return True
