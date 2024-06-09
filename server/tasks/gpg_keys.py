import logging
from uuid import UUID

from celery import shared_task

from config import Database
from dec import init_user
from gnupg import GPG
from models.hashcat_request import User
from schemas import CeleryResponse

db = Database()
logger = logging.getLogger(__name__)


@shared_task(name="server.get_pubkey")
def get_pubkey():
    try:
        gpg = GPG()
        key_identifier = "muclicat@deiteriy.com"
        logger.debug("Exporting keys for %s", key_identifier)
        public_keys = gpg.export_keys(key_identifier)
        if public_keys:
            return CeleryResponse(
                value=public_keys.encode("utf-8"), error="", warning=""
            ).model_dump()
        else:
            return CeleryResponse(
                error="Public key not found.", value=None, warning=""
            ).model_dump()
    except Exception as e:
        logger.error(
            "An error occurred while exporting keys: %s", str(e), exc_info=True
        )
        return CeleryResponse(
            error=f"An error occurred while exporting keys: {str(e)}",
            warning="",
            value=None,
        ).model_dump()


@shared_task(name="server.upload_user_pubkey")
@init_user(db.session)
def upload_user_pubkey(owner_id: UUID, pubkey: str):
    with db.session() as session:
        user = session.query(User).filter(User.id == owner_id).first()
        if user is None:
            return CeleryResponse(
                value=None, warning="", error="Cannot create user"
            ).model_dump()
        user.pubkey = pubkey

    return CeleryResponse(value="User public key update successful", warning="", error="").model_dump()
