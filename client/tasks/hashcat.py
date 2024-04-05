import logging

from celery import current_task, shared_task
from config import Config, Database
from hashcat import FileManager, HashcatExecutor, HashcatDiscreteTaskContainer
from hashcat.hashcat import Hashcat
from schemas import HashcatDiscreteTask

logger = logging.getLogger(__name__)
db = Database(Config.get("DATABASE_URL"))
file_manager = FileManager(Config.get("RULES_DIR"), Config.get("WORDLISTS_DIR"))
hashcat = Hashcat()
hashcat_executor = HashcatExecutor(file_manager, hashcat)


@shared_task(name="client.run_hashcat", ignore_result=True)
def run_hashcat(discrete_task_as_dict):
    discrete_task = HashcatDiscreteTask(**discrete_task_as_dict)
    worker_id = current_task.request.hostname
    wordlists = file_manager.get_wordlists_files()
    rules = file_manager.get_rules_files()

    success = hashcat_executor.execute(discrete_task)

    ...


@shared_task(name="client.calc_keyspace", ignore_result=False)
def calc_keyspace(keyspace_task):
    c = HashcatDiscreteTaskContainer.model_validate({"task": keyspace_task})
    return c.task.calc_keyspace(hashcat_executor).dict()


@shared_task(name="b.benchmark", ignore_result=True)
def benchmark(hash_modes=None):
    results = hashcat_executor.benchmark(hash_modes)

    # TODO: write results to the backend

    ...
