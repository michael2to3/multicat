import logging

from celery import shared_task

from config import Database, UUIDGenerator
from db import DatabaseHelper, StepManager
from schemas import CeleryResponse

logger = logging.getLogger(__name__)


db = Database()


@shared_task(name="server.delete_steps")
def delete_steps(user_id: str, step_name: int):
    user_id = str(UUIDGenerator.generate(user_id))
    with db.session() as session:
        manager = StepManager(user_id, session)
        manager.delete_steps(step_name)
        return CeleryResponse(value="Step deleted successfully").model_dump()


@shared_task(name="server.get_steps")
def get_steps(user_id: str, step_name: str):
    user_id = str(UUIDGenerator.generate(user_id))
    with db.session() as session:
        manager = StepManager(user_id, session)
        yaml_dump = manager.get_steps(step_name)
        return CeleryResponse(value=yaml_dump).model_dump()


@shared_task(name="server.list_steps")
def list_steps(user_id: str):
    user_id = str(UUIDGenerator.generate(user_id))
    with db.session() as session:
        manager = StepManager(user_id, session)
        steps_name = manager.list_steps()
        return CeleryResponse(value=steps_name).model_dump()


@shared_task(name="server.load_steps")
def load_steps(user_id: str, steps_name: str, yaml_content: str):
    user_id = str(UUIDGenerator.generate(user_id))
    with db.session() as session:
        manager = StepManager(user_id, session)
        manager.load_steps(steps_name, yaml_content)
        return CeleryResponse(value=f"{steps_name} saved successfully").model_dump()


@shared_task
def post_load_steps(keyspaces, user_id: str = "", steps_name: str = ""):
    with db.session() as session:
        for keyspace_dict in keyspaces:
            ks = Keyspace(**keyspace_dict)
            session.add(ks)

        db_helper = DatabaseHelper(session)
        step = db_helper.get_steps(user_id, steps_name)
        step.is_keyspace_calculated = True
        session.commit()

    # TODO: Notify user about what happend (not in the world)
