import logging
from datetime import timedelta

from celery import current_app, shared_task, current_task
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from config import Config, Database
from models import HashcatAsset
from schemas import CeleryResponse, HashcatAssetSchema

db = Database(Config.get("DATABASE_URL"))


def fetch_assets_by_uuid(task_uuid):
    with db.session() as session:
        result = (
            session.query(HashcatAsset)
            .filter(HashcatAsset.task_uuid == task_uuid)
            .filter(HashcatAsset.timestamp >= (func.now() - timedelta(minutes=2)))
            .all()
        )
        assets_data = [HashcatAssetSchema.from_orm(asset).dict() for asset in result]
        return assets_data


def get_active_workers():
    current_worker = current_task.request.hostname
    return [
        x for x in current_app.control.inspect().stats().keys() if x != current_worker
    ]


def fetch_assets_by_worker_name(worker_name):
    with db.session() as session:
        asset = (
            session.query(HashcatAsset)
            .filter(HashcatAsset.worker_id == worker_name)
            .first()
        )
        return HashcatAssetSchema.from_orm(asset)


@shared_task(name="main.collect_assets")
def collect_assets(owner_id: str):
    active_workers = get_active_workers()
    if len(active_workers) == 0:
        return CeleryResponse(
            warning="No workers are currently active, try again later"
        )

    try:
        data = [fetch_assets_by_worker_name(x.split("@")[0]) for x in active_workers]
        if len(data) != 0:
            return CeleryResponse(value=data).dict()

    except SQLAlchemyError as e:
        logging.error(f"Database error occurred: {e}")
        return CeleryResponse(error="Database error occurred").dict()
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return CeleryResponse(error="An unexpected error occurred").dict()

    task = current_app.send_task(
        "b.get_assets",
        args=("",),
        exchange="broadcast_exchange",
        routing_key="broadcast",
    )
    task.forget()
    return CeleryResponse(
        warning="No assets found within the time limit, initiated broadcast task"
    ).dict()
