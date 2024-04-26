import logging

from sqlalchemy import update, bindparam
from celery import current_task, shared_task

import models
from config import Config, Database
from filemanager.assets_filemanager import AssetsFileManager
from hashcat import HashcatBenchmark, HashcatKeyspace, HashcatBruteforce
from hashcat.hashcat import Hashcat
from schemas import HashcatDiscreteTask, KeyspaceBase, get_keyspace_adapter, HashIdMapping, HashCrackedValueMapping

logger = logging.getLogger(__name__)
db = Database(Config().database_url)
file_manager = AssetsFileManager()
hashcat = Hashcat()
hashcat_keyspace = HashcatKeyspace(file_manager, hashcat)
hashcat_benchmark = HashcatBenchmark(file_manager, hashcat)


def fetch_uncracked_hashes(job_id: int) -> list[HashIdMapping]:
    with db.session() as session:
        res = (
            session.query(models.Hash.id, models.Hash.value)
            .join(models.Hash.related_jobs)
            .filter(models.Job.id == job_id)
            .filter(models.Hash.is_cracked == False)
            .all()
        )
        return [HashIdMapping(id=x[0], hash=x[1]) for x in res]


def upload_results(uncracked: list[HashIdMapping], results: list[HashCrackedValueMapping]):
    uncracked_map = {m.hash: m.id for m in uncracked}
    upresults = [
        {
            "id": uncracked_map[res.hash],
            "cracked_value": res.cracked_value,
        }
        for res in results
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
    hashes = [m.hash for m in uncracked]

    hashcat_bruteforce = HashcatBruteforce(
        file_manager, hashcat, discrete_task, keyspace_schema, hashes
    )

    rc = hashcat_bruteforce.execute()
    results = hashcat_bruteforce.read_results()
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
