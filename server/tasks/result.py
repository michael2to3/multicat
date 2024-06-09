import logging
from typing import cast
from uuid import UUID

from celery import shared_task

from config import Database
from db.database_helper import DatabaseHelper
from dec import init_user
from gnupg import GPG, Verify
from models.hashcat_request import Hash, Job
from schemas.codegen.task_and_steps import CeleryResponse

db = Database()
logger = logging.getLogger(__name__)
gpg = GPG()


@shared_task(name="server.get_result")
@init_user(db.session)
def get_result(owner_id: UUID, job_id: UUID):
    with db.session() as session:
        dbh = DatabaseHelper(session)
        user = dbh.get_or_create_user(owner_id)
        pubkey = cast(str, user.pubkey)

        if not pubkey:
            return CeleryResponse(
                error="User has no public key for encryption.", warning="", value=None
            ).model_dump()

        import_result = gpg.import_keys(pubkey)
        logger.info("GPG import result: %s", import_result.results)
        if not import_result.count:
            logger.error("Failed to import public key: %s", pubkey)
            return CeleryResponse(
                error="Failed to import public key", warning="", value=None
            ).model_dump()

        fingerprint = import_result.fingerprints[0]
        logger.info("Using fingerprint for encryption: %s", fingerprint)

        trust_result = gpg.trust_keys(fingerprint, 'TRUST_ULTIMATE')
        logger.info("GPG trust result: %s", trust_result)

        job = session.query(Job).filter(Job.id == job_id).first()
        if job is None:
            logger.error("Job %s not found", job)
            return CeleryResponse(
                error="Job not found", warning="", value=None
            ).model_dump()

        hashes = (
            session.query(Hash)
            .join(Job, Hash.related_jobs)
            .filter(Job.id == job_id)
            .all()
        )

        if not hashes:
            return CeleryResponse(
                error="No hashes found for job {}".format(job_id),
                warning="",
                value=None,
            ).model_dump()

        result = [
            f"{hash.value}:{hash.cracked_value}"
            for hash in hashes
            if cast(bool, hash.is_cracked)
        ]

        encrypted_data = gpg.encrypt("\n".join(result), fingerprint)
        if encrypted_data.ok:
            encrypted_result = encrypted_data.data.decode("utf-8")
            return CeleryResponse(
                value=encrypted_result, error="", warning=""
            ).model_dump()
        else:
            logger.error("GPG Encryption failed: %s", encrypted_data.status)
            logger.error("GPG stderr: %s", encrypted_data.stderr)
            return CeleryResponse(
                error="Failed to encrypt data", warning="", value=None
            ).model_dump()
