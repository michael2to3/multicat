import logging
from typing import Dict

from hashcat.filemanager import FileManager
from hashcat.interface import HashcatInterface

from .executor_base import HashcatExecutorBase

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class HashcatDevicesInfoException(Exception):
    pass


class HashcatDevices(HashcatExecutorBase):
    def __init__(self, file_manager: FileManager, hashcat: HashcatInterface):
        self._file_manager = file_manager
        self._hashcat = hashcat

    def devices_info(self) -> Dict:
        self._hashcat.reset()
        self._hashcat.no_threading = True
        self._hashcat.quiet = True
        self._hashcat.backend_info = True

        rc = self._hashcat.hashcat_session_init()

        if rc < 0:
            logger.error("Hashcat: %s", self._hashcat.hashcat_status_get_log())
            raise HashcatDevicesInfoException("Failed to gather devices info")

        return self._hashcat.get_backend_devices_info()
