import uuid
import logging

from celery import signature
from celery.signals import worker_init, worker_process_init
from config import CeleryApp, Config, Database
from tasks.assets import _refresh_assets

app = CeleryApp("client").get_app()
app.autodiscover_tasks(["tasks"], force=True)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@worker_init.connect
def setup_essentials(*args, **kwargs):
    db = Database(Config.get("DATABASE_URL"))
    logger.info("Database initialized.")

    _refresh_assets(uuid.UUID("d0f82c66-d08c-581d-9098-8b1f33341a4e"), worker_id=Config.get("WORKER_NAME"))


@worker_process_init.connect
def setup_database(*args, **kwargs):
    pass
