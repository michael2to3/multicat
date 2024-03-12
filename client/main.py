import logging
import asyncio
from celery import current_task
from models import HashcatAsset
from schemas import Request, HashcatOption
from hashcat import HashcatManager, HashcatException, FileManager
from config import CeleryApp, Config, Database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


app = CeleryApp("client").get_app()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
file_manager = FileManager(Config.get("RULES_DIR"), Config.get("WORDLISTS_DIR"))

db = Database(Config.get("DATABASE_URL"))


@app.task(name="b.get_wordlists", bind=True, ignore_result=True)
def get_wordlists(self, task_uuid):
    worker_id = current_task.request.hostname
    wordlists = file_manager.get_wordlists_files()

    with db.session() as session:
        hashcat_asset = HashcatAsset(
            task_uuid=task_uuid, worker_id=worker_id, wordlists=wordlists, rules=[]
        )
        session.add(hashcat_asset)

    logger.info(f"Wordlists for worker {worker_id} saved to DB.")


@app.task
def get_rules():
    return file_manager.get_rules_files()


@app.task(bind=True)
def run_hashcat(self, request: dict):
    request_model = Request(**request)
    manager = HashcatManager("hashcat", file_manager)

    manager.add_option(HashcatOption.ATTACK_MODE, request_model.mode.mode_num)

    if request_model.wordlists is not None:
        for wordlist in request_model.wordlists:
            manager.add_option(HashcatOption.WORDLIST_FILE, wordlist)

    if request_model.masks is not None:
        for mask in request_model.masks:
            manager.add_option(HashcatOption.MASK, mask)

    if request_model.rules_files is not None:
        for rules_file in request_model.rules_files:
            manager.add_option(
                HashcatOption.RULES_FILE, file_manager.get_rule(rules_file)
            )

    loop = asyncio.get_event_loop()
    try:
        result = loop.run_until_complete(manager.run())
        return result
    except HashcatException as e:
        self.update_state(
            state="FAILURE", meta={"exc_type": type(e).__name__, "exc_message": str(e)}
        )
        raise e
