import json
import logging

import yaml
from celery import shared_task
from pydantic import ValidationError, parse_obj_as
from sqlalchemy.exc import SQLAlchemyError

from config import Database, UUIDGenerator
from models import HashcatStep, Step, User, UserRole
from schemas import CeleryResponse, Steps, hashcat_step_loader

logger = logging.getLogger(__name__)


db = Database()


def get_user(session, user_id: str):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        user = User(id=user_id, role=UserRole.USER.value)
        session.add(user)
        session.commit()
    return user


@shared_task(name="main.delete_steps")
def delete_steps(user_id: str, namerule: int):
    user_id = UUIDGenerator.generate(user_id)
    with db.session() as session:
        user = get_user(session, user_id)
        step = (
            session.query(Step)
            .filter(Step.name == namerule, Step.user_id == user.id)
            .first()
        )
        if step:
            session.delete(step)
            session.commit()
            return CeleryResponse(value="Step deleted successfully").dict()
        else:
            return CeleryResponse(error="Step not found.").dict()


@shared_task(name="main.get_steps")
def get_steps(user_id: str, step_name: str):
    user_id = UUIDGenerator.generate(user_id)
    with db.session() as session:
        user = get_user(session, user_id)

        step = (
            session.query(Step)
            .filter(Step.user_id == user_id, Step.name == step_name)
            .first()
        )
        if not step:
            return CeleryResponse(error="Step not found.").dict()

        hashcat_steps = [json.loads(s.value) for s in step.hashcat_steps]

        yaml_dump = yaml.dump(
            hashcat_steps, default_flow_style=False, allow_unicode=True
        )
        return CeleryResponse(value=yaml_dump).dict()


@shared_task(name="main.list_steps")
def list_steps(user_id: str):
    user_id = UUIDGenerator.generate(user_id)
    with db.session() as session:
        user = get_user(session, user_id)

        steps = session.query(Step.name).filter(Step.user_id == user_id).all()
        steps_name = [step.name for step in steps]

        if steps_name:
            return CeleryResponse(value=steps_name).dict()
        else:
            return CeleryResponse(error="No steps found.").dict()


@shared_task(name="main.load_steps")
def load_steps(user_id: str, steps_name: str, yaml_content: str):
    user_id = UUIDGenerator.generate(user_id)
    with db.session() as session:
        user = get_user(session, user_id)

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
            step = Step(name=steps_name, user_id=user.id)
            for hashcat_steps_model in model.steps:
                hashcat_steps = HashcatStep(value=hashcat_steps_model.json())
                step.hashcat_steps.append(hashcat_steps)
            session.add(step)
            session.commit()

            return CeleryResponse(value=f"{steps_name} saved successfully").dict()
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Database error while saving steps: {str(e)}")
            return CeleryResponse(error=f"Database error: {str(e)}").dict()
