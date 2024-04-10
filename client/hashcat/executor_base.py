import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class HashcatExecutorBase:
    def check_hexec(self) -> bool:
        rc = self.hashcat.hashcat_session_execute()
        if rc < 0:
            logger.error("Hashcat: %s", self.hashcat.hashcat_status_get_log())
            return False

        return True
