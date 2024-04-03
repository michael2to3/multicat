import logging
import yaml

from datetime import datetime, UTC
from typing import Dict

from celery import shared_task

from config import Database
from models import DatabaseHelper
from schemas import CeleryResponse

db = Database()
logger = logging.getLogger(__name__)


@shared_task(name="server.get_devices")
def get_devices():
    data = {}
    with db.session() as session:
        db_helper = DatabaseHelper(session)
        db_helper.get_devices()

        for devices in db_helper.get_devices():
            data[devices.worker_name] = devices.value

    return CeleryResponse(value=yaml.dump(data)).model_dump()


def get_generic_devices(obj):
    if not obj:
        return []

    # cuda/hip
    if dev := obj.get("devices"):
        return dev
    # ocl
    elif plat := obj.get("platforms"):
        devices = []
        for x in plat:
            if devs := x.get("devices"):
                devices.extend(devs)

        return devices
    else:
        return []


def devices_info_match(before, after) -> bool:
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


@shared_task(name="server.update_devices_info", ignore_result=True)
def update_devices_info(worker_name: str, devices_new_dict: Dict):
    with db.session() as session:
        db_helper = DatabaseHelper(session)
        devices = db_helper.get_worker_devices(worker_name)

        if not devices:
            db_helper.add_devices_info(worker_name, devices_new_dict)
            logger.info("Device info for worker %s has been added", worker_name)
            return

        if not devices_info_match(devices.value, devices_new_dict):
            logger.info("Device info for worker %s has been updated", worker_name)
            devices.value = devices_new_dict

        devices.timestamp = datetime.now(UTC)
        session.commit()
