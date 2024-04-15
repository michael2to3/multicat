import logging

from celery.signals import worker_init, worker_process_init

from config import CeleryApp, Config, Database
from config.config import ConfigKey
from tasks.devices import _update_devices

app = CeleryApp("client").get_app()
app.autodiscover_tasks(["tasks"], force=True)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@worker_init.connect
def setup_essentials(*args, **kwargs):
    _update_devices()


@worker_process_init.connect
def setup_database(*args, **kwargs):
    Database(Config.get(ConfigKey.DATABASE_URL))
    logger.info("Database initialized.")
