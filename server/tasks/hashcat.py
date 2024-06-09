import base64
import io
import logging
from uuid import UUID

from celery import shared_task

import gnupg
import schemas
from config import Database
from dec import init_user
from hashcat_distributor import (
    BruteforceConfigurationManager,
    BruteforceTasksGenerator,
    HashPreprocessor,
)
from models.hashcat_request import Job, JobStatus

db = Database()
logger = logging.getLogger(__name__)


@shared_task(name="server.bruteforce_finished")
def bruteforce_finished(
    rcs,
    job_id: UUID,
):
    with db.session() as session:
        job: Job = session.query(Job).filter(Job.id == job_id).first()
        if job is None:
            logger.error("Job %s not found", job_id)

        job.status = JobStatus.COMPLETED.value

    # TODO: Schedule loopback
    # TODO: Send results to the user
    logger.info("%d job has been finished", job_id)


@shared_task(name="server.run_hashcat")
@init_user(db.session)
def run_hashcat(
    owner_id: UUID, hashtype: str, step_name: str, base64_encrypt_hashes: str
):
    gpg = gnupg.GPG()

    encrypt_hashes = base64.b64decode(base64_encrypt_hashes)
    hashes_in_memory = io.BytesIO(encrypt_hashes)

    decrypted_data = gpg.decrypt_file(hashes_in_memory)

    if not decrypted_data.ok:
        return schemas.CeleryResponse(
            error="Failed to decrypt the file", warning="", value=None
        ).model_dump()

    hashes = decrypted_data.data
    if not hashes:
        return schemas.CeleryResponse(
            error="Hashes are empty", warning="", value=None
        ).model_dump()

    hashes = [i for i in hashes.decode("utf-8").split("\n") if i]

    hp = HashPreprocessor(hashtype)
    hashes = hp.preprocess(hashes)

    with db.session() as session:
        try:
            dts = BruteforceConfigurationManager(
                owner_id, step_name, hashtype, hashes, session
            )
            steps, job, hash_type = dts.get_new_configuration()

            BruteforceTasksGenerator.send_bruteforce_tasks(steps, job, hash_type)

            return schemas.CeleryResponse(
                value=job.id, error="", warning=""
            ).model_dump()
        except ValueError as e:
            logger.error(e, exc_info=True)
            return schemas.CeleryResponse(
                error=str(e), warning="", value=None
            ).model_dump()
