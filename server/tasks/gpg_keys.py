from gnupg import GPG
from celery import shared_task
from schemas import CeleryResponse


@shared_task(name="main.get_pubkey")
def get_pubkey():
    try:
        gpg = GPG()
        key_identifier = "muclicat@deiteriy.com"
        public_keys = gpg.export_keys(key_identifier)
        if public_keys:
            return CeleryResponse(value=public_keys.encode("utf-8")).dict()
        else:
            return CeleryResponse(error="Public key not found.").dict()
    except Exception as e:
        return CeleryResponse(
            error=f"An error occurred while exporting keys: {str(e)}"
        ).dict()
