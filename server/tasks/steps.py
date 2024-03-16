import logging
import yaml
import json
from pydantic import ValidationError, parse_obj_as
from celery import shared_task
from schemas import hashcat_step_constructor, Steps, HashcatStep
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError, parse_obj_as
from schemas import Steps, hashcat_step_loader
from models import StepsModel, get_unique_name_hashcatrules
from config import Database, UUIDGenerator

from pydantic.dataclasses import dataclass
from pydantic import TypeAdapter
import dataclasses
import json


logger = logging.getLogger(__name__)


@shared_task(name="main.delsteps")
def delsteps(owner_id, namerule):
    db_instance = Database()
    try:
        uid = UUIDGenerator.generate(owner_id)
    except ValueError as ve:
        logger.error(f"Invalid UUID format: {str(ve)}")
        return f"Invalid UUID format: {str(ve)}"

    try:
        with db_instance.session() as session:
            query = session.query(StepsModel).filter(
                StepsModel.owner_id == uid, StepsModel.name == namerule
            )
            steps = query.first()
            if steps:
                session.delete(steps)
                try:
                    session.commit()
                    logger.info("StepsModel deleted successfully")
                    return "StepsModel deleted successfully"
                except SQLAlchemyError as e:
                    logger.error(f"Database delete operation failed: {str(e)}")
                    return f"Database delete operation failed: {str(e)}"
            else:
                return "Rule not found."
    except Exception as e:
        logger.error(f"Failed to retrieve steps: {str(e)}")
        return f"Failed to retrieve steps: {str(e)}"


@shared_task(name="main.getsteps")
def getsteps(owner_id, namerule):
    db_instance = Database()
    try:
        uid = UUIDGenerator.generate(owner_id)
    except ValueError as ve:
        logger.error(f"Invalid UUID format: {str(ve)}")
        return f"Invalid UUID format: {str(ve)}"

    try:
        with db_instance.session() as session:
            query = session.query(StepsModel.steps).filter(
                StepsModel.owner_id == uid, StepsModel.name == namerule
            )
            steps_data = query.first()
            if steps_data:
                steps_dict = dict(steps_data.steps) if steps_data.steps else {}
                return yaml.dump(
                    steps_dict, default_flow_style=False, allow_unicode=True
                )
            else:
                return "Rule not found."

    except Exception as e:
        logger.error(f"Failed to retrieve steps: {str(e)}")
        return f"Failed to retrieve steps: {str(e)}"


@shared_task(name="main.liststeps")
def liststeps(owner_id):
    db_instance = Database()
    try:
        uid = UUIDGenerator.generate(owner_id)
    except ValueError as ve:
        logger.error(f"Invalid UUID format: {str(ve)}")
        return f"Invalid UUID format: {str(ve)}"

    try:
        with db_instance.session() as session:
            query = (
                session.query(StepsModel.name)
                .filter(StepsModel.owner_id == uid)
                .distinct()
            )
            steps_name = [rule_name for (rule_name,) in query]
            return steps_name
    except Exception as e:
        logger.error(f"Failed to retrieve steps: {str(e)}")
        return f"Failed to retrieve steps: {str(e)}"


@shared_task(name="main.loadsteps")
def loadsteps(owner_id, namerule, rule):
    try:
        data = yaml.load(rule, Loader=hashcat_step_loader())
        model = parse_obj_as(Steps, data)
    except yaml.YAMLError as ye:
        logger.error(f"Failed to load YAML content: {str(ye)}")
        return f"Failed to load YAML content: {str(ye)}"
    except ValidationError as ve:
        logger.error(f"Validation error for the provided data: {str(ve)}")
        return f"Validation error for the provided data: {str(ve)}"

    steps_json = model.json()

    db_instance = Database()
    with db_instance.session() as session:
        new_step = StepsModel(
            owner_id=UUIDGenerator.generate(owner_id),
            name=get_unique_name_hashcatrules(session, namerule),
            steps=json.loads(steps_json),
        )
        session.add(new_step)
        try:
            session.commit()
            logger.info("StepsModel saved successfully")
            return "StepsModel saved successfully"
        except SQLAlchemyError as e:
            logger.error(f"Database save operation failed: {str(e)}")
            return f"Database save operation failed: {str(e)}"
