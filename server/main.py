from celery import Celery
import celeryconfig
from db import DatabaseOperations, ConnectedClient
from celery.schedules import crontab
from datetime import datetime, timedelta
import logging

app = Celery("server")
app.config_from_object(celeryconfig)
app.autodiscover_tasks(["tasks"], force=True)
db = DatabaseOperations()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app.conf.beat_schedule = {
    "cleanup-inactive-clients-every-5-minutes": {
        "task": "cleanup_inactive_clients",
        "schedule": crontab(minute="*/5"),
    },
}


@app.task(name="register_client")
def register_client(client_id):
    db.register_client(client_id)


@app.task(name="unregister_client")
def unregister_client(client_id):
    db.unregister_client(client_id)


@app.task
def cleanup_inactive_clients():
    with db.get_connection() as conn:
        inactive_threshold = datetime.now() - timedelta(minutes=5)
        stmt = ConnectedClient.delete().where(
            ConnectedClient.c.last_heartbeat < inactive_threshold
        )
        conn.execute(stmt)
    logger.info("Inactive clients cleaned up.")
