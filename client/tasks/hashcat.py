import logging
from typing import Dict, List, Tuple

from sqlalchemy import update, bindparam
from celery import current_task, shared_task

import models
from config import Config, Database
from filemanager.assets_filemanager import AssetsFileManager
from hashcat import HashcatBenchmark, HashcatKeyspace, HashcatBruteforce
from hashcat.hashcat import Hashcat
from schemas import HashcatDiscreteTask, KeyspaceBase, get_keyspace_adapter

logger = logging.getLogger(__name__)
db = Database(Config().database_url)
file_manager = AssetsFileManager()
hashcat = Hashcat()
hashcat_keyspace = HashcatKeyspace(file_manager, hashcat)
hashcat_benchmark = HashcatBenchmark(file_manager, hashcat)


def fetch_uncracked_hashes(job_id: int) -> List[Tuple[int, str]]:
    with db.session() as session:
        return (
            session.query(models.Hash.id, models.Hash.value)
            .join(models.Hash.related_jobs)
            .filter(models.Job.id == job_id)
            .filter(models.Hash.is_cracked == False)
            .all()
        )


def upload_results(uncracked: List[Tuple[int, str]], results: Dict[str, str]):
    uncracked_map = {}
    for id, hash in uncracked:
        uncracked_map[hash] = id

    upresults = [
        {
            "id": uncracked_map[hash],
            "cracked_value": cracked_value,
        }
        for hash, cracked_value in results.items()
    ]

    with db.session() as session:
        stmt = update(models.Hash).values(
            cracked_value=bindparam("cracked_value"), is_cracked=True
        )
        session.execute(
            stmt,
            upresults,
        )


@shared_task(name="client.run_hashcat")
def run_hashcat(discrete_task_as_dict, keyspace_as_dict):
    discrete_task = HashcatDiscreteTask(**discrete_task_as_dict)
    keyspace_schema: KeyspaceBase = get_keyspace_adapter().validate_python(
        keyspace_as_dict
    )

    logger.info("Processing %d job", discrete_task.job_id)

    worker_id = current_task.request.hostname
    uncracked = fetch_uncracked_hashes(discrete_task.job_id)
    hashes = [h for _, h in uncracked]

    hashcat_bruteforce = HashcatBruteforce(
        file_manager, hashcat, discrete_task, keyspace_schema, hashes
    )
    rc, results = hashcat_bruteforce.execute()
    if results:
        upload_results(uncracked, results)

    logger.info("Finished processing %d job: %d", discrete_task.job_id, rc)
    return rc


@shared_task(name="client.calc_keyspace", ignore_result=False)
def calc_keyspace(keyspace_task) -> int:
    try:
        keyspace_schema: KeyspaceBase = get_keyspace_adapter().validate_python(
            keyspace_task
        )
        return hashcat_keyspace.calc_keyspace(keyspace_schema)
    except Exception as e:
        logger.error("Error in calc_keyspace: %s", e)
        return -1


@shared_task(name="b.benchmark", ignore_result=True)
def benchmark(hash_modes):
    results = hashcat_benchmark.benchmark(hash_modes)

    # TODO: write results to the backend

    ...
