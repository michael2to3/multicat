import logging

from celery import current_task, shared_task
from config import Config, Database
from hashcat import FileManager, HashcatExecutor
from models import HashcatAsset
from schemas import HashcatDiscreteTask, HashcatStep

logger = logging.getLogger(__name__)
db = Database(Config.get("DATABASE_URL"))
file_manager = FileManager(Config.get("RULES_DIR"), Config.get("WORDLISTS_DIR"))
hashcat_executor = HashcatExecutor(file_manager)


@shared_task(name="client.run_hashcat", ignore_result=True)
def run_hashcat(discrete_task_as_dict):
    discrete_task = HashcatDiscreteTask(**discrete_task_as_dict)
    worker_id = current_task.request.hostname
    wordlists = file_manager.get_wordlists_files()
    rules = file_manager.get_rules_files()

    success = hashcat_executor.execute(discrete_task)

    ...


@shared_task(name = "client.calc_keyspace")
def calc_keyspace(keyspace_task):
    step = HashcatStep(**keyspace_task)
    return hashcat_executor.calc_keyspace(step)
