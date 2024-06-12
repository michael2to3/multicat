import base64
import io
import logging
from uuid import UUID

from celery import shared_task
from sqlalchemy.orm import scoped_session

import gnupg
import models
import schemas
from config import Database
from db.database_helper import DatabaseHelper
from dec import init_user
from hashcat_distributor import (
    BruteforceConfigurationManager,
    BruteforceTasksGenerator,
    HashPreprocessor,
)
from models.hashcat_request import Job, JobStatus
from steps.retriever import StepRetriever
from yamlutils.yaml_step_loader import yaml_step_loader

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
        dbh = DatabaseHelper(session)
        try:
            steps = _load_steps(session, owner_id, step_name)
            hashtype = dbh.get_or_create_hashtype_as_model(hashtype)

            job = _create_job(session, owner_id)
            dts = BruteforceConfigurationManager(job, hashtype, hashes, session)

            job = dts.get_new_configuration()

            BruteforceTasksGenerator.send_bruteforce_tasks(steps, job, hashtype)

            return schemas.CeleryResponse(
                value=job.id, error="", warning=""
            ).model_dump()
        except ValueError as e:
            logger.error(e, exc_info=True)
            return schemas.CeleryResponse(
                error="Failed to load steps", warning="", value=None
            ).model_dump()


def _load_steps(
    session: scoped_session, owner_id: UUID, step_name: str
) -> schemas.Steps:
    # @fixme https://git.t00x.com/Tools/multicat/issues/59
    manager = StepRetriever(owner_id, session)
    yaml_content = manager.get_orig_dump(step_name)
    data = yaml_step_loader().load(yaml_content)
    steps = schemas.Steps(**data)
    return steps


def _create_job(session: scoped_session, owner_id: UUID) -> models.Job:
    dbh = DatabaseHelper(session)
    user: models.User = dbh.get_or_create_user(owner_id)
    return models.Job(owning_user=user)
