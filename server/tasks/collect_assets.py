import logging
import uuid
from celery import chord, shared_task, current_app
from celery.signals import worker_process_init
from sqlalchemy.future import select
from models import HashcatAsset
from schemas import HashcatAssetSchema
from config import CeleryApp, Config, Database
from sqlalchemy import func
from datetime import timedelta

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
def collect_assets(uid: str):
    task_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, uid)
    data = fetch_assets_by_uuid(task_uuid)
    if data and len(data) != 0:
        return data

    task = current_app.send_task(
        "b.get_assets",
        args=(str(task_uuid),),
        exchange="broadcast_exchange",
        routing_key="broadcast",
    )
    return data

@shared_task
def run_hashcat():
    pass
