import logging
from typing import List
from uuid import UUID

from celery import shared_task

from config import Database
from db import DatabaseHelper
from schemas import CeleryResponse
from steps import StepDeleter, StepLoadFacade, StepRetriever
from steps.save_keyspace import SaveKeyspacesTask

logger = logging.getLogger(__name__)


db = Database()


@shared_task(name="server.delete_steps")
def delete_steps(user_id: UUID, step_name: str):
    with db.session() as session:
        manager = StepDeleter(user_id, session)
        manager.delete_step(step_name)
        session.commit()
        return CeleryResponse(value="Step deleted successfully").model_dump()


@shared_task(name="server.get_steps")
def get_steps(user_id: UUID, step_name: str):
    with db.session() as session:
        manager = StepRetriever(user_id, session)
        hashcat_steps = manager.get_steps(step_name)
        return CeleryResponse(value=hashcat_steps).model_dump()


@shared_task(name="server.get_orig_steps")
def get_orig_steps(user_id: UUID, step_name: str):
    with db.session() as session:
        manager = StepRetriever(user_id, session)
        original_content = manager.get_orig_steps(step_name)
        return CeleryResponse(value=original_content).model_dump()


@shared_task(name="server.list_steps")
def list_steps(user_id: UUID):
    with db.session() as session:
        manager = StepRetriever(user_id, session)
        steps_name = manager.get_steps_names()
        return CeleryResponse(value=steps_name).model_dump()


@shared_task(name="server.load_steps")
def load_steps(user_id: UUID, steps_name: str, yaml_content: str):
    message = "Processing..."
    with db.session() as session:
        facade = StepLoadFacade(user_id, session)
        message = facade.process_steps(steps_name, yaml_content)
    return CeleryResponse(value=message).model_dump()


@shared_task(name="server.save_keyspaces")
def save_keyspaces(keyspaces, unknown_keyspaces: List, user_id: UUID, steps_name: str):
    with db.session() as session:
        dbh = DatabaseHelper(session)
        task = SaveKeyspacesTask(session, dbh)
        task.execute(keyspaces, unknown_keyspaces, user_id, steps_name)
        session.commit()


@shared_task(name="server.clenaup_on_error")
def clenaup_on_error(userid: UUID, steps_name: str):
    with db.session() as session:
        deleter = StepDeleter(userid, session)
        deleter.delete_step(steps_name)
        session.commit()
