import logging
from uuid import UUID

from celery import shared_task
from config import Database
from db import DatabaseHelper
from dec import init_user
from schemas import CeleryResponse
from steps import StepDeleter, StepLoadFacade, StepRetriever
from steps.save_keyspace import SaveKeyspacesTask

logger = logging.getLogger(__name__)


db = Database()


@shared_task(name="server.delete_steps")
@init_user(db.session)
def delete_steps(user_id: UUID, step_name: str):
    with db.session() as session:
        manager = StepDeleter(user_id, session)
        manager.delete_step(step_name)
        session.commit()
        return CeleryResponse(value="Step deleted successfully").model_dump()


@shared_task(name="server.get_steps")
@init_user(db.session)
def get_steps(user_id: UUID, step_name: str):
    with db.session() as session:
        manager = StepRetriever(user_id, session)
        hashcat_steps = manager.get_steps(step_name)
        return CeleryResponse(value=hashcat_steps).model_dump()


@shared_task(name="server.get_orig_steps")
@init_user(db.session)
def get_orig_steps(user_id: UUID, step_name: str):
    with db.session() as session:
        manager = StepRetriever(user_id, session)
        original_content = manager.get_orig_steps(step_name)
        return CeleryResponse(value=original_content).model_dump()


@shared_task(name="server.list_steps")
@init_user(db.session)
def list_steps(user_id: UUID):
    with db.session() as session:
        manager = StepRetriever(user_id, session)
        steps_name = manager.get_steps_names()
        return CeleryResponse(value=steps_name).model_dump()


@shared_task(name="server.load_steps")
@init_user(db.session)
def load_steps(user_id: UUID, steps_name: str, yaml_content: str):
    message = "Processing..."
    with db.session() as session:
        facade = StepLoadFacade(user_id, session)
        message = facade.process_steps(steps_name, yaml_content)
    return CeleryResponse(value=message).model_dump()


@shared_task(name="server.save_keyspaces")
@init_user(db.session)
def save_keyspaces(user_id: UUID, keyspaces, unknown_keyspaces: list, steps_name: str):
    with db.session() as session:
        dbh = DatabaseHelper(session)
        task = SaveKeyspacesTask(session, dbh)
        task.execute(keyspaces, unknown_keyspaces, user_id, steps_name)
        session.commit()


@shared_task(name="server.clenaup_on_error")
@init_user(db.session)
def clenaup_on_error(user_id: UUID, steps_name: str):
    with db.session() as session:
        deleter = StepDeleter(user_id, session)
        deleter.delete_step(steps_name)
        session.commit()
