import logging

from celery import current_task, shared_task
from config import Config, Database
from hashcat import FileManager
from models import HashcatAsset

logger = logging.getLogger(__name__)
db = Database(Config.get("DATABASE_URL"))
file_manager = FileManager(Config.get("RULES_DIR"), Config.get("WORDLISTS_DIR"))


@shared_task(name="b.get_assets", ignore_result=True)
def get_assets(task_uuid):
    worker_id = current_task.request.hostname
    wordlists = file_manager.get_wordlists_files()
    rules = file_manager.get_rules_files()

    with db.session() as session:
        hashcat_asset = HashcatAsset(
            task_uuid=task_uuid, worker_id=worker_id, wordlists=wordlists, rules=rules
        )
        session.add(hashcat_asset)

    logger.info(f"Asset added to database: {hashcat_asset}")
