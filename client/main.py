import uuid
import logging

from celery import signature
from celery.signals import worker_init, worker_process_init
from config import CeleryApp, Config, Database
from hashcat.filemanager import FileManager
from hashcat.hashcat import Hashcat
from hashcat.hashcat_executor import HashcatExecutor
from tasks.devices import _update_devices

app = CeleryApp("client").get_app()
app.autodiscover_tasks(["tasks"], force=True)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
file_manager = FileManager(Config.get("RULES_DIR"), Config.get("WORDLISTS_DIR"))
hashcat = Hashcat()
hashcat_executor = HashcatExecutor(file_manager, hashcat)


@worker_init.connect
def setup_essentials(*args, **kwargs):
    _update_devices()


@worker_process_init.connect
def setup_database(*args, **kwargs):
    Database(Config.get("DATABASE_URL"))
    logger.info("Database initialized.")
