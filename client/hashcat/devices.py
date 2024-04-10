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
        self.file_manager = file_manager
        self.hashcat = hashcat

    def devices_info(self) -> Dict:
        self.hashcat.reset()
        self.hashcat.no_threading = True
        self.hashcat.quiet = True
        self.hashcat.backend_info = True

        rc = self.hashcat.hashcat_session_init()

        if rc < 0:
            logger.error("Hashcat: %s", self.hashcat.hashcat_status_get_log())
            raise HashcatDevicesInfoException("Failed to gather devices info")

        return self.hashcat.get_backend_devices_info()
