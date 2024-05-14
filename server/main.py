import logging

from celery.signals import worker_process_init

from config import CeleryApp, Config, Database

config = Config()
app = CeleryApp("server").get_app()
app.autodiscover_tasks(["tasks"], force=True)


def logger_setup() -> None:
    logger_level = getattr(logging, config.logger_level.upper(), logging.INFO)
    logging.basicConfig(level=logger_level)


@worker_process_init.connect
def setup_database(*args, **kwargs):
    Database(config.database_url)


if __name__ == "__main__":
    logger_setup()
