import yaml

from celery import current_app, shared_task, current_task

from config import Database
from models import DatabaseHelper
from schemas import CeleryResponse

db = Database()


def get_active_workers():
    current_worker = current_task.request.hostname
    return [
        x for x in current_app.control.inspect().stats().keys() if x != current_worker
    ]


@shared_task(name="server.get_devices")
def get_devices():
    active_workers = get_active_workers()
    if len(active_workers) == 0:
        return CeleryResponse(
            warning="No workers are currently active, try again later"
        )

    data = {}

    with db.session() as session:
        db_helper = DatabaseHelper(session)
        for worker in active_workers:
            devices = db_helper.get_worker_devices(worker.split("@")[0])
            if devices:
                data[worker] = devices

    return CeleryResponse(value=yaml.dump(data)).dict()
