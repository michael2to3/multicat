import logging
from datetime import timedelta

from celery import current_app, shared_task
from config import Config, Database, UUIDGenerator
from models import HashcatAsset
from schemas import CeleryResponse, HashcatAssetSchema
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)
db = Database(Config.database_url)


def fetch_assets_by_uuid(task_uuid):
    with db.session() as session:
        result = (
            session.query(HashcatAsset)
            .filter(HashcatAsset.task_uuid == task_uuid)
            .filter(HashcatAsset.timestamp >= (func.now() - timedelta(minutes=2)))
            .all()
        )
        assets_data = [
            HashcatAssetSchema.model_validate(asset).model_dump() for asset in result
        ]
        return assets_data


@shared_task(name="main.collect_assets")
def collect_assets(owner_id: str):
    task_uuid = UUIDGenerator.generate(owner_id)

    task = current_app.send_task("b.get_assets", args=(str(task_uuid),))
    task.forget()

    try:
        data = fetch_assets_by_uuid(task_uuid)
        if data:
            return CeleryResponse(value=data).model_dump()

    except SQLAlchemyError as e:
        logging.error(f"Database error occurred: {e}")
        return CeleryResponse(error="Database error occurred").model_dump()
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return CeleryResponse(error="An unexpected error occurred").model_dump()

    return CeleryResponse(
        warning="No assets found within the time limit, initiated broadcast task"
    ).model_dump()
