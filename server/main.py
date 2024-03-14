import logging
from celery.signals import worker_process_init
from config import CeleryApp, Config, Database

app = CeleryApp("server").get_app()
app.autodiscover_tasks(["tasks"], force=True)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

db = None


@worker_process_init.connect
def setup_database(*args, **kwargs):
    global db
    db = Database(Config.get("DATABASE_URL"))
    logger.info("Database initialized.")
