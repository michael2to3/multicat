import json
import logging
from typing import List

import yaml
from celery import shared_task, chord, signature
from pydantic import ValidationError, parse_obj_as
from sqlalchemy.exc import SQLAlchemyError

from common import DiscreteTasksGenerator
from config import Database, UUIDGenerator
from models import DatabaseHelper, HashcatStep, Step, Keyspace
from schemas import CeleryResponse, Steps, hashcat_step_loader

logger = logging.getLogger(__name__)


db = Database()


@shared_task(name="server.delete_steps")
def delete_steps(user_id: str, step_name: int):
    user_id = UUIDGenerator.generate(user_id)
    with db.session() as session:
        db_helper = DatabaseHelper(session)
        user = db_helper.get_or_create_user(str(user_id))
        step = (
            session.query(Step)
            .filter(
                Step.name == step_name,
                Step.user_id == user.id,
                Step.is_keyspace_calculated == True,
            )
            .first()
        )
        if step:
            session.delete(step)
            session.commit()
            return CeleryResponse(value="Step deleted successfully").dict()
        else:
            return CeleryResponse(error="Step not found.").dict()


@shared_task(name="server.get_steps")
def get_steps(user_id: str, step_name: str):
    user_id = UUIDGenerator.generate(user_id)
    with db.session() as session:
        db_helper = DatabaseHelper(session)
        user = db_helper.get_or_create_user(str(user_id))

        step = (
            session.query(Step)
            .filter(
                Step.user_id == user_id,
                Step.name == step_name,
                Step.is_keyspace_calculated == True,
            )
            .first()
        )
        if not step:
            return CeleryResponse(error="Step not found.").dict()

        hashcat_steps = [json.loads(s.value) for s in step.hashcat_steps]

        yaml_dump = yaml.dump(
            hashcat_steps, default_flow_style=False, allow_unicode=True
        )
        return CeleryResponse(value=yaml_dump).dict()


@shared_task(name="server.list_steps")
def list_steps(user_id: str):
    user_id = UUIDGenerator.generate(user_id)
    with db.session() as session:
        db_helper = DatabaseHelper(session)
        user = db_helper.get_or_create_user(user_id)

        steps = session.query(Step.name).filter(Step.user_id == user_id, Step.is_keyspace_calculated == True).all()
        steps_name = [step.name for step in steps]

        if steps_name:
            return CeleryResponse(value=steps_name).dict()
        else:
            return CeleryResponse(error="No steps found.").dict()


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


@shared_task
def on_chord_error(request, exc, traceback):
    # TODO: remove failed keyspace computation
    logger.error("Task {0!r} raised error: {1!r}".format(request.id, exc))


def calculate_unknown_keyspaces(user_id: str, steps_name: str, unkown_keyspaces: List):
    pass
    callback = post_load_steps.subtask(
        kwargs={"user_id": user_id, "steps_name": steps_name},
        queue="server",
    )
    group_tasks = [
        signature("client.calc_keyspace", args=(task.model_dump(),))
        for task in unkown_keyspaces
    ]
    chord(group_tasks, callback).on_error(on_chord_error.s()).apply_async()


@shared_task(name="server.load_steps")
def load_steps(user_id: str, steps_name: str, yaml_content: str):
    user_id = UUIDGenerator.generate(user_id)
    with db.session() as session:
        db_helper = DatabaseHelper(session)
        user = db_helper.get_or_create_user(user_id)

        try:
            data = yaml.load(yaml_content, Loader=hashcat_step_loader())
            model = parse_obj_as(Steps, data)
        except yaml.YAMLError as e:
            logger.error(f"Failed to load YAML content: {str(e)}")
            return CeleryResponse(error=f"Failed to load YAML content: {str(e)}").dict()
        except ValidationError as e:
            logger.error(f"Validation error for the provided data: {str(e)}")
            return CeleryResponse(
                error=f"Validation error for the provided data: {str(e)}"
            ).dict()

        try:
            unkown_keyspaces = []
            dt_generator = DiscreteTasksGenerator(model)
            for discrete_task in dt_generator.yield_discrete_tasks():
                if not db_helper.keyspace_exists(**discrete_task.model_dump()):
                    unkown_keyspaces.append(discrete_task)

            step = Step(name=steps_name, user_id=user.id)
            for hashcat_steps_model in model.steps:
                hashcat_steps = HashcatStep(value=hashcat_steps_model.json())
                step.hashcat_steps.append(hashcat_steps)

            msg = f"{steps_name} saved successfully"
            if unkown_keyspaces:
                step.is_keyspace_calculated = False
                calculate_unknown_keyspaces(user_id, steps_name, unkown_keyspaces)
                msg = f"Some of the keyspaces are new for the steps {steps_name}. Steps are saved but are not listed for now. I'll be back"
            else:
                step.is_keyspace_calculated = True

            session.add(step)
            session.commit()

            return CeleryResponse(value=msg).dict()
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Database error while saving steps: {str(e)}")
            return CeleryResponse(error=f"Database error: {str(e)}").dict()
