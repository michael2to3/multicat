import logging
from datetime import timedelta

from celery import current_app, shared_task, current_task
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from config import Config, Database, UUIDGenerator
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


@shared_task(name="main.collect_assets")
def collect_assets(owner_id: str):
    task_uuid = UUIDGenerator.generate(owner_id)
    try:
        data = fetch_assets_by_uuid(task_uuid)
        if data:
            return CeleryResponse(value=data).dict()

    except SQLAlchemyError as e:
        logging.error(f"Database error occurred: {e}")
        return CeleryResponse(error="Database error occurred").dict()
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return CeleryResponse(error="An unexpected error occurred").dict()

    task = current_app.send_task(
        "b.get_assets",
        args=(str(task_uuid),),
        exchange="broadcast_exchange",
        routing_key="broadcast",
    )
    task.forget()
    return CeleryResponse(
        warning="No assets found within the time limit, initiated broadcast task"
    ).dict()
