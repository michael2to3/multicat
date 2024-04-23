import base64
import io
import logging
from typing import List
from uuid import UUID

from celery import shared_task, chord, signature
from models.hashcat_request import Hash
from schemas.discrete_task import Steps
from schemas.hashcat_helpers import hashcat_step_loader
from sqlalchemy.orm import scoped_session
from sqlalchemy import func, and_

import gnupg
import models
import schemas
from config import Database
from db import DatabaseHelper
from steps.loader import KeyspaceCalculator
from steps.retriever import StepRetriever

db = Database()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@shared_task(name="server.bruteforce_finished")
def bruteforce_finished(
    rcs,
    job_id: int,
):
    logger.info("%d job has been finished", job_id)


def send_discrete_task(
    owner_id: UUID,
    step_name: str,
    hashtype: str,
    hashes: List[str],
    session: scoped_session,
):
    db_helper = DatabaseHelper(session)

    manager = StepRetriever(owner_id, session)
    yaml_content = manager.get_orig_steps(step_name)
    data = hashcat_step_loader().load(yaml_content)
    steps = Steps(**data)

    hash_type: schemas.HashType = db_helper.get_or_create_hashtype_as_schema(hashtype)
    session.commit()

    user: models.User = db_helper.get_or_create_user(owner_id)
    job = models.Job(owning_user=user)

    unnested = func.unnest(hashes).alias("hash_view")
    existing: List[Hash] = session.query(Hash).select_from(unnested).filter(and_(Hash.hash_type == hash_type, Hash.value == unnested.column)).all()

    for hash in existing:
        hash.related_jobs.append(job)

        hashes.remove(hash.value)

    for i in hashes:
        models.Hash(hash_type=hash_type, related_jobs=[job], value=i)

    session.add(job)
    session.flush()

    tasks = []
    for keyspace in KeyspaceCalculator.generate_keyspace_tasks(steps):
        task_data = schemas.HashcatDiscreteTask(
            job_id=job.id,
            hash_type=schemas.HashType(
                hashcat_type=hash_type.hashcat_type,
                human_readable=hash_type.human_readable,
            ),
        )
        tasks.append(
            signature("client.run_hashcat", args=(task_data.model_dump(), keyspace.model_dump()))
        )

    callback = signature(
        "server.bruteforce_finished",
        queue="server",
        kwargs={
            "job_id": job.id,
        },
    )

    chord(tasks)(callback)
    return job.id


def preprocess_lm_ntlm_pwdump(hashes: List[str], hashtype):
    sample = hashes[0]
    sep = ":"
    if len(sample.split(sep)) != 7:
        return

    sep_idx = 3 if hashtype == "1000" else 2
    for i, hash in enumerate(hashes):
        hashes[i] = hash.split(sep)[sep_idx]


def preprocess_hashes(hashes: List[str], hashtype):
    if hashtype in ["1000", "3000"]:
        preprocess_lm_ntlm_pwdump(hashes, hashtype)

    return list(set(hashes))


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
    hashes = preprocess_hashes(hashes, hashtype)

    with db.session() as session:
        try:
            job_id = send_discrete_task(owner_id, step_name, hashtype, hashes, session)
        except ValueError as e:
            return schemas.CeleryResponse(error=str(e)).model_dump()

    # TODO: messages about write commands in the agent, the server does not known about it
    message = f"Your task has been queued and will start as soon as a server becomes available. You can check the progress of your task using the command /status {job_id}. Thank you for your patience."

    return schemas.CeleryResponse(value=message).model_dump()
