import base64
import io
from typing import List
from uuid import UUID

from celery import current_app, shared_task
from sqlalchemy.orm import scoped_session

import gnupg
import models
import schemas
from config import Database
from db import DatabaseHelper

db = Database()


def send_discrete_task(
    owner_id: UUID,
    step_name: str,
    hashtype: str,
    hashes: List[str],
    session: scoped_session,
):
    db_helper = DatabaseHelper(session)
    step = db_helper.get_hashcat_steps(owner_id, step_name)
    hash_type: schemas.HashType = db_helper.get_or_create_hashtype_as_schema(hashtype)
    user: models.User = db_helper.get_or_create_user(owner_id)
    job = models.Job(owning_user=user)
    for i in hashes:
        models.Hash(hash_type=hash_type, parent_job=job, value=i)

    session.add(job)
    session.flush()
    for step in step.steps:
        task_data = schemas.HashcatDiscreteTask(
            job_id=job.id,
            step=step,
            hash_type=schemas.HashType(
                hashcat_type=hash_type.hashcat_type,
                human_readable=hash_type.human_readable,
            ),
            hashes=hashes,
        )
        task = current_app.send_task(
            "client.run_hashcat", args=(task_data.model_dump(),)
        )
        task.forget()

    return job.id


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
    with db.session() as session:
        try:
            job_id = send_discrete_task(owner_id, step_name, hashtype, hashes, session)
        except ValueError as e:
            return schemas.CeleryResponse(error=str(e)).model_dump()

    # TODO: messages about write commands in the agent, the server does not known about it
    message = f"Your task has been queued and will start as soon as a server becomes available. You can check the progress of your task using the command /status {job_id}. Thank you for your patience."

    return schemas.CeleryResponse(value=message).model_dump()
