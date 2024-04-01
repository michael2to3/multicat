import logging

from datetime import datetime
from celery import current_task, shared_task

from config import Config, Database
from hashcat import FileManager, HashcatExecutor
from models import HashcatAsset

logger = logging.getLogger(__name__)
db = Database(Config.get("DATABASE_URL"))
file_manager = FileManager(Config.get("RULES_DIR"), Config.get("WORDLISTS_DIR"))
hashcat_executor = HashcatExecutor(file_manager)


class WorkerIsNotFoundException(Exception):
    pass


def _refresh_assets(task_uuid: str, worker_id: str):
    wordlists = file_manager.get_wordlists_files()
    rules = file_manager.get_rules_files()

    with db.session() as session:
        hashcat_asset = (
            session.query(HashcatAsset)
            .filter(HashcatAsset.worker_id==worker_id)
            .first()
        )

        if not hashcat_asset:
            hashcat_asset = HashcatAsset(
                task_uuid=task_uuid, worker_id=worker_id, wordlists=wordlists, rules=rules
            )
            session.add(hashcat_asset)
            logger.info("Asset added to database: %s", hashcat_asset)
        else:
            hashcat_asset.rules = rules
            hashcat_asset.wordlists = wordlists
            hashcat_asset.timestamp=datetime.utcnow()
            session.commit()
            logger.info("Asset updated: %s", hashcat_asset)


@shared_task(name="b.get_assets", ignore_result=True)
def get_assets(task_uuid: str):
    # worker_id = current_task.request.hostname
    worker_id = Config.get("WORKER_NAME")
    _refresh_assets(task_uuid, worker_id)


def devices_info_match(before, after) -> bool:
    def get_generic_devices(obj):
        if not obj:
            return []

        # cuda/hip
        if dev := obj.get('devices'):
            return dev
        # ocl
        elif plat := obj.get('platforms'):
            devices = []
            for x in plat:
                if devs := x.get("devices"):
                    devices.extend(devs)

            return devices
        else:
            return []

    if len(before) != len(after):
        return False

    devices_before = []
    for x in ["cuda", "hip", "ocl"]:
        devices_before += get_generic_devices(before.get(x))

    devices_after = []
    for x in ["cuda", "hip", "ocl"]:
        devices_after += get_generic_devices(after.get(x))

    if len(devices_before) != len(devices_after):
        return False

    checks = ["device_id", "device_name", "device_processors"]

    for bd, ad in zip(devices_before, devices_after):
        for check in checks:
            if bd[check] != ad[check]:
                return False

    return True


def _update_devices_info(worker_id: str):
    db = Database(Config.get("DATABASE_URL"))
    devices = hashcat_executor.devices_info()

    with db.session() as session:
        asset = (
            session.query(HashcatAsset)
            .filter(HashcatAsset.worker_id == worker_id)
            .first()
        )

        if not asset:
            raise WorkerIsNotFoundException("Worker asset hasn't been found: %s" % worker_id)

        if not asset.devices:
            asset.devices = devices
            asset.benchmarks = None
            asset.timestamp = datetime.utcnow()
            session.commit()
            logger.info(f"Worker devices info added: %s" % worker_id)
            return

        if not devices_info_match(asset.devices, devices):
            asset.devices = devices
            asset.benchmarks = None
            asset.timestamp = datetime.utcnow()
            session.commit()
            logger.info(f"Worker devices info updated: %s" % worker_id)
            return

        asset.timestamp=datetime.utcnow()
        session.commit()
