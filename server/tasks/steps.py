import logging
from typing import List
from uuid import UUID

import yaml
from celery import shared_task
from pydantic import ValidationError

from config import Database, UUIDGenerator
from db import DatabaseHelper
from models.keyspaces import Keyspace
from schemas import CeleryResponse, Steps, hashcat_step_loader
from schemas.keyspaces import get_keyspace_adapter
from steps import StepDeleter, StepFacade, StepRetriever
from visitor.keyspace_to_model import KeyspaceModelCreator

logger = logging.getLogger(__name__)


db = Database()


@shared_task(name="server.delete_steps")
def delete_steps(user_id: UUID, step_name: int):
    with db.session() as session:
        manager = StepDeleter(user_id, session)
        manager.delete_step(step_name)
        session.commit()
        return CeleryResponse(value="Step deleted successfully").model_dump()


@shared_task(name="server.get_steps")
def get_steps(user_id: UUID, step_name: str):
    with db.session() as session:
        manager = StepRetriever(user_id, session)
        yaml_dump = manager.get_steps(step_name)
        return CeleryResponse(value=yaml_dump).model_dump()


@shared_task(name="server.list_steps")
def list_steps(user_id: UUID):
    with db.session() as session:
        manager = StepRetriever(user_id, session)
        steps_name = manager.list_steps()
        return CeleryResponse(value=steps_name).model_dump()


@shared_task(name="server.load_steps")
def load_steps(user_id: UUID, steps_name: str, yaml_content: str):
    try:
        loader = hashcat_step_loader()
        data = loader.load(yaml_content)
        steps = Steps(**data)
    except (yaml.YAMLError, ValidationError) as e:
        logger.error(f"Error loading and validating steps: {str(e)}")
        raise
    except TypeError as e:
        logger.error("Failed to instantiate steps: %s", str(e))
        logger.debug("Data reveived: %s", yaml_content)
        raise

    with db.session() as session:
        facade = StepFacade(user_id, session)
        facade.load_and_calculate_steps(steps_name, steps)
        session.commit()
        return CeleryResponse(
            value=f"{steps_name} loaded and processed successfully"
        ).model_dump()


@shared_task(name="server.post_load_steps")
def post_load_steps(keyspaces, unkown_keyspaces: List, user_id: UUID, steps_name: str):
    with db.session() as session:
        for keyspace, value in zip(unkown_keyspaces, keyspaces):
            keyspace["value"] = value
            keyspace_schema = get_keyspace_adapter().validate_python(keyspace)

            def callback(keyspace_model: Keyspace):
                session.add(keyspace_model)

            visitor = KeyspaceModelCreator(callback, {})
            keyspace_schema.accept(visitor)

        db_helper = DatabaseHelper(session)
        step = db_helper.get_steps(user_id, steps_name)
        step.is_keyspace_calculated = True
        session.commit()

    # TODO: Notify user about what happend (not in the world)


@shared_task
def on_chord_error(request, exc, traceback):
    # TODO: remove failed keyspace computation
    logger.error("Task {0!r} raised error: {1!r}".format(request.id, exc))
