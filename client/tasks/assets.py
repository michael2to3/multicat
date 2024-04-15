import logging
from datetime import UTC, datetime

from celery import shared_task

from config import Config, Database
from config.config import ConfigKey
from filemanager.assets_filemanager import AssetsFileManager
from models import HashcatAsset

logger = logging.getLogger(__name__)
db = Database(Config.get(ConfigKey.DATABASE_URL))
file_manager = AssetsFileManager()


def _refresh_assets(task_uuid: str, worker_id: str):
    files = file_manager.get_all_files()

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
                files=files,
            )
            session.add(hashcat_asset)
            logger.info("Asset added to database: %s", hashcat_asset)
        else:
            hashcat_asset.files = files
            hashcat_asset.timestamp = datetime.now(UTC)
            logger.info("Asset updated: %s", hashcat_asset)
        session.commit()


@shared_task(name="b.get_assets", ignore_result=True)
def get_assets(task_uuid: str):
    worker_id = Config.get("WORKER_NAME")
    _refresh_assets(task_uuid, worker_id)
