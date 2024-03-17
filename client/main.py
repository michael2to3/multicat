import logging
import asyncio
from celery import current_task
from models import HashcatAsset
from schemas import Request
from hashcat import FileManager
from config import CeleryApp, Config, Database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


app = CeleryApp("client").get_app()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
file_manager = FileManager(Config.get("RULES_DIR"), Config.get("WORDLISTS_DIR"))

db = Database(Config.get("DATABASE_URL"))


@app.task(name="b.get_assets", bind=True, ignore_result=True)
def get_assets(self, task_uuid):
    worker_id = current_task.request.hostname
    wordlists = file_manager.get_wordlists_files()
    rules = file_manager.get_rules_files()

    with db.session() as session:
        hashcat_asset = HashcatAsset(
            task_uuid=task_uuid, worker_id=worker_id, wordlists=wordlists, rules=rules
        )
        session.add(hashcat_asset)

    logger.info(f"Asset added to database: {hashcat_asset}")


@app.task(bind=True)
def run_hashcat(self, request: dict):
    request_model = Request(**request)
    pass
