import json
import logging

import yaml
from celery import chord, signature
from pydantic import ValidationError
from sqlalchemy.orm import Session

from db import DatabaseHelper
from generator import DiscreteTasksGenerator
from models import Step
from schemas import Steps, hashcat_step_loader

logger = logging.getLogger(__name__)


class StepManager:
    def __init__(self, user_id: str, session: Session):
        self.user_id = user_id
        self.session = session
        self.db_helper = DatabaseHelper(session)

    def delete_steps(self, step_name: int):
        user = self.db_helper.get_or_create_user(self.user_id)
        step = (
            self.session.query(Step)
            .filter(
                Step.name == step_name,
                Step.user_id == user.id,
                Step.is_keyspace_calculated,
            )
            .first()
        )
        if not step:
            raise ValueError("Step not found.")

        self.session.delete(step)
        self.session.commit()

    def get_steps(self, step_name: str):
        user = self.db_helper.get_or_create_user(self.user_id)
        step = (
            self.session.query(Step)
            .filter(
                Step.user_id == self.user_id,
                Step.name == step_name,
                Step.is_keyspace_calculated,
            )
            .first()
        )
        if not step:
            raise ValueError("Step not found.")

        hashcat_steps = [json.loads(s.value) for s in step.hashcat_steps]
        yaml_dump = yaml.dump(
            hashcat_steps, default_flow_style=False, allow_unicode=True
        )
        return yaml_dump

    def list_steps(self):
        user = self.db_helper.get_or_create_user(self.user_id)
        steps = (
            self.session.query(Step.name)
            .filter(Step.user_id == user.id, Step.is_keyspace_calculated)
            .all()
        )
        steps_name = [step.name for step in steps]

        if not steps_name:
            raise ValueError("No steps found.")

        return steps_name

    def load_steps(self, steps_name: str, yaml_content: str):
        try:
            data = yaml.load(yaml_content, Loader=hashcat_step_loader())
            model = Steps(**data)
        except (yaml.YAMLError, ValidationError) as e:
            logger.error(f"Error loading steps: {str(e)}")
            raise

        unkown_keyspaces = []
        for discrete_task in self._generate_task(model):
            if not self.db_helper.keyspace_exists(**discrete_task.model_dump()):
                logger.info(f"Unknown keyspace: {discrete_task}")
                unkown_keyspaces.append(discrete_task)

        step = Step(name=steps_name, user_id=self.user_id, is_keyspace_calculated=False)
        self.session.add(step)
        self.session.commit()

        if unkown_keyspaces:
            self._calculate_and_save_unknown_keyspaces(unkown_keyspaces, steps_name)

    def _calculate_and_save_unknown_keyspaces(self, unkown_keyspaces, steps_name: str):
        logger.info(f"Unknown keyspaces found: {unkown_keyspaces}")
        tasks = [
            signature("client.calc_keyspace", args=(discrete_task.model_dump(),))
            for discrete_task in unkown_keyspaces
        ]
        callback = signature(
            "server.post_load_steps",
            kwargs={"user_id": self.user_id, "steps_name": steps_name},
        )
        chord(tasks)(callback)

    def _generate_task(self, model: Steps):
        for step in model.steps:
            for task in DiscreteTasksGenerator.generate_tasks(step):
                yield task
