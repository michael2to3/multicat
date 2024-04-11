import logging

import yaml
from celery import chord, signature
from pydantic import ValidationError
from sqlalchemy.orm import scoped_session

from db import DatabaseHelper
from generator import KeyspaceGenerator
from models import Step
from models.hashcat_request import HashcatStep
from schemas import Steps, hashcat_step_loader

logger = logging.getLogger(__name__)


class StepLoader:
    def __init__(self, user_id: str, session: scoped_session):
        self.db_helper = DatabaseHelper(session)
        self.session = session
        self.user_id = user_id

    def load_steps(self, steps_name: str, yaml_content: str):
        try:
            data = yaml.load(yaml_content, Loader=hashcat_step_loader())
            steps = Steps(**data)
        except (yaml.YAMLError, ValidationError) as e:
            logger.error(f"Error loading steps: {str(e)}")
            raise

        is_keyspace_calculated, unknown_keyspaces = self._process_keyspaces(steps)

        step = Step(
            name=steps_name,
            user_id=self.user_id,
            is_keyspace_calculated=is_keyspace_calculated,
        )
        self.session.add(step)
        self._add_hashcat_steps(step, steps)

        if unknown_keyspaces:
            self._calculate_and_save_unknown_keyspaces(unknown_keyspaces, steps_name)

    def _process_keyspaces(self, steps):
        is_keyspace_calculated = True
        unknown_keyspaces = []
        for keyspace_task in self._generate_keyspace_tasks(steps):
            if not self.db_helper.keyspace_exists(keyspace_task):
                is_keyspace_calculated = False
                unknown_keyspaces.append(keyspace_task)
        return is_keyspace_calculated, unknown_keyspaces

    def _add_hashcat_steps(self, step, steps):
        for hashcat_task in steps.steps:
            hashcat_step_value = hashcat_task.model_dump_json()
            existing_hashcat_step = (
                self.session.query(HashcatStep)
                .filter(HashcatStep.value == hashcat_step_value)
                .first()
            )
            if existing_hashcat_step:
                hashcat_step_model = existing_hashcat_step
            else:
                hashcat_step_model = HashcatStep(value=hashcat_step_value)

            if hashcat_step_model not in step.hashcat_steps:
                step.hashcat_steps.append(hashcat_step_model)
                if not existing_hashcat_step:
                    self.session.add(hashcat_step_model)

        self.session.commit()

    def _calculate_and_save_unknown_keyspaces(self, unknown_keyspaces, steps_name):
        logger.info(f"Unknown keyspaces found: {unknown_keyspaces}")
        tasks = [
            signature("client.calc_keyspace", args=(keyspace_task.model_dump(),))
            for keyspace_task in unknown_keyspaces
        ]
        callback = signature(
            "server.post_load_steps",
            queue="server",
            kwargs={
                "unkown_keyspaces": [x.model_dump() for x in unknown_keyspaces],
                "user_id": self.user_id,
                "steps_name": steps_name,
            },
        )
        chord(tasks)(callback)

    def _generate_keyspace_tasks(self, model: Steps):
        for step in model.steps:
            for task in KeyspaceGenerator.generate_tasks(step):
                yield task
