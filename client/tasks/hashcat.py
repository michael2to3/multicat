import logging

from celery import current_task, shared_task

from config import Config, Database
from filemanager.assets_filemanager import AssetsFileManager
from hashcat import HashcatBenchmark, HashcatKeyspace
from hashcat.hashcat import Hashcat
from schemas import HashcatDiscreteTask, KeyspaceBase, get_keyspace_adapter

logger = logging.getLogger(__name__)
db = Database(Config().database_url)
file_manager = AssetsFileManager()
hashcat = Hashcat()
hashcat_keyspace = HashcatKeyspace(file_manager, hashcat)
hashcat_benchmark = HashcatBenchmark(file_manager, hashcat)


@shared_task(name="client.run_hashcat", ignore_result=True)
def run_hashcat(discrete_task_as_dict):
    discrete_task = HashcatDiscreteTask(**discrete_task_as_dict)
    worker_id = current_task.request.hostname

    logger.debug(
        "discrete_task: %s, worker_id: %s, wordlists: %s, rules: %s",
        discrete_task,
        worker_id,
    )


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
