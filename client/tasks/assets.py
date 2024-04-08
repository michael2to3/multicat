import logging
from datetime import UTC, datetime

from celery import shared_task

from config import Config, Database
from hashcat import FileManager
from models import HashcatAsset

logger = logging.getLogger(__name__)
db = Database(Config.get("DATABASE_URL"))
file_manager = FileManager(Config.get("RULES_DIR"), Config.get("WORDLISTS_DIR"))


def _refresh_assets(task_uuid: str, worker_id: str):
    wordlists = file_manager.get_wordlists_files()
    rules = file_manager.get_rules_files()

    with db.session() as session:
        hashcat_asset = (
            session.query(HashcatAsset)
            .filter(HashcatAsset.worker_id == worker_id)
            .first()
        )

        if not hashcat_asset:
            hashcat_asset = HashcatAsset(
                task_uuid=task_uuid,
                worker_id=worker_id,
                wordlists=wordlists,
                rules=rules,
            )
            session.add(hashcat_asset)
            logger.info("Asset added to database: %s", hashcat_asset)
        else:
            hashcat_asset.rules = rules
            hashcat_asset.wordlists = wordlists
            hashcat_asset.timestamp = datetime.now(UTC)
            session.commit()
            logger.info("Asset updated: %s", hashcat_asset)


@shared_task(name="b.get_assets", ignore_result=True)
def get_assets(task_uuid: str):
    worker_id = Config.get("WORKER_NAME")
    _refresh_assets(task_uuid, worker_id)
