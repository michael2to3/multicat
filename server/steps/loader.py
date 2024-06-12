import logging
from uuid import UUID

from celery import chord, signature
from sqlalchemy.orm import scoped_session

import models
from db import DatabaseHelper
from hashcat_distributor.keyspace_tasks_generator import KeyspaceTasksGenerator
from models.hashcat_request import HashcatStep
from schemas import Steps, StepStatus
from schemas.keyspaces import KeyspaceBase

logger = logging.getLogger(__name__)


class StepLoader:
    def __init__(self, user_id: UUID, session: scoped_session):
        self._dbh = DatabaseHelper(session)
        self._session = session
        self._user_id = user_id

    def load_steps(self, steps_name: str, steps: Steps, original_content: str):
        stepinfo = models.Step(
            name=steps_name,
            user_id=self._user_id,
            original_content=original_content,
            status=StepStatus.PROCESSING.value,
        )
        self._session.add(stepinfo)
        self._add_hashcat_steps(stepinfo, steps)

    def _add_hashcat_steps(self, step: models.Step, steps_data: Steps):
        for hashcat_task in steps_data.steps:
            hashcat_step_value = hashcat_task.model_dump_json()
            hashcat_step_model = (
                self._session.query(HashcatStep)
                .filter(HashcatStep.value == hashcat_step_value)
                .first()
            )

            if hashcat_step_model is None:
                hashcat_step_model = HashcatStep(value=hashcat_step_value)
                self._session.add(hashcat_step_model)

            if hashcat_step_model not in step.hashcat_steps:
                step.hashcat_steps.append(hashcat_step_model)


class KeyspaceCalculator:
    def __init__(
        self, db_helper: DatabaseHelper, session: scoped_session, user_id: UUID
    ):
        self._dbh = db_helper
        self._session = session
        self._user_id = user_id

    def calculate_and_save_unknown_keyspaces(self, steps: Steps, steps_name: str):
        unknown_keyspaces = self._process_keyspaces(steps)
        tasks = [
            signature("client.calc_keyspace", args=(keyspace_task.model_dump(),))
            for keyspace_task in unknown_keyspaces
        ]
        callback = signature(
            "server.save_keyspaces",
            queue="server",
            kwargs={
                "user_id": self._user_id,
                "unknown_keyspaces": [x.model_dump() for x in unknown_keyspaces],
                "steps_name": steps_name,
            },
        )
        chord(tasks)(callback)

    def _process_keyspaces(self, steps) -> list[KeyspaceBase]:
        unknown_keyspaces: list[KeyspaceBase] = []
        for keyspace_task in KeyspaceTasksGenerator.generate_keyspace_tasks(steps):
            if not self._dbh.keyspace_exists(keyspace_task):
                unknown_keyspaces.append(keyspace_task)
        return unknown_keyspaces
