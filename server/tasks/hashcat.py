import base64
import io
import logging
from uuid import UUID

import gnupg
from celery import shared_task

import schemas
from config import Database
from common import HashPreprocessor, DiscreteTasksSender

db = Database()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@shared_task(name="server.bruteforce_finished")
def bruteforce_finished(
    rcs,
    job_id: int,
):
    # TODO: Schedule loopback
    # TODO: Send results to the user
    logger.info("%d job has been finished", job_id)


@shared_task(name="server.run_hashcat")
def run_hashcat(
    owner_id: UUID, hashtype: str, step_name: str, base64_encrypt_hashes: str
):
    gpg = gnupg.GPG()

    encrypt_hashes = base64.b64decode(base64_encrypt_hashes)
    hashes_in_memory = io.BytesIO(encrypt_hashes)

    decrypted_data = gpg.decrypt_file(hashes_in_memory)

    if not decrypted_data.ok:
        return schemas.CeleryResponse(error="Failed to decrypt the file").model_dump()

    hashes = decrypted_data.data
    if not hashes:
        return schemas.CeleryResponse(error="Hashes are empty").model_dump()

    hashes = [i for i in hashes.decode("utf-8").split("\n") if i]

    hp = HashPreprocessor(hashtype)
    hashes = hp.preprocess(hashes)

    with db.session() as session:
        try:
            dts = DiscreteTasksSender(owner_id, step_name, hashtype, hashes, session)
            job_id = dts.send_discrete_tasks()
        except ValueError as e:
            return schemas.CeleryResponse(error=str(e)).model_dump()

    # TODO: messages about write commands in the agent, the server does not known about it
    message = f"Your task has been queued and will start as soon as a server becomes available. You can check the progress of your task using the command /status {job_id}. Thank you for your patience."

    return schemas.CeleryResponse(value=message).model_dump()
