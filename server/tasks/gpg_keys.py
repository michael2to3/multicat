from celery import shared_task

from gnupg import GPG
from schemas import CeleryResponse


@shared_task(name="server.get_pubkey")
def get_pubkey():
    try:
        gpg = GPG()
        key_identifier = "muclicat@deiteriy.com"
        public_keys = gpg.export_keys(key_identifier)
        if public_keys:
            return CeleryResponse(value=public_keys.encode("utf-8")).model_dump()
        else:
            return CeleryResponse(error="Public key not found.").model_dump()
    except Exception as e:
        return CeleryResponse(
            error=f"An error occurred while exporting keys: {str(e)}"
        ).model_dump()
