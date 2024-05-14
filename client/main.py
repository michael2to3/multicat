import logging

from celery.signals import worker_init, worker_process_init
from config import CeleryApp, Config, Database
from tasks.devices import _update_devices

config = Config()
app = CeleryApp("client").get_app()
app.autodiscover_tasks(["tasks"], force=True)


def logger_setup() -> None:
    logger_level = getattr(logging, config.logger_level.upper(), logging.INFO)
    logging.basicConfig(level=logger_level)


@worker_init.connect
def setup_essentials(*args, **kwargs):
    _update_devices()


@worker_process_init.connect
def setup_database(*args, **kwargs):
    Database(config.database_url)


if __name__ == "main":
    logger_setup()
