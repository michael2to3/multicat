import logging

from celery import shared_task

from gnupg import GPG
from schemas import CeleryResponse

logger = logging.getLogger(__name__)


@shared_task(name="server.get_pubkey")
def get_pubkey():
    try:
        gpg = GPG()
        key_identifier = "muclicat@deiteriy.com"
        logger.debug("Exporting keys for %s", key_identifier)
        public_keys = gpg.export_keys(key_identifier)
        if public_keys:
            return CeleryResponse(value=public_keys.encode("utf-8")).model_dump()
        else:
            return CeleryResponse(error="Public key not found.").model_dump()
    except Exception as e:
        logger.error("An error occurred while exporting keys: %s", str(e), exc_info=True)
        return CeleryResponse(
            error=f"An error occurred while exporting keys: {str(e)}"
        ).model_dump()
