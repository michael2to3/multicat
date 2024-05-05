import logging
from typing import List
from uuid import UUID

from sqlalchemy.orm import scoped_session

from db import DatabaseHelper
from models.hashcat_request import Step
from schemas import StepStatus
from keyspace import get_keyspace_adapter
from visitor.keyspace_to_model import KeyspaceModelCreator

logger = logging.getLogger(__name__)


class SaveKeyspacesTask:
    def __init__(self, session: scoped_session, db_helper: DatabaseHelper):
        self._session = session
        self._dbh = db_helper

    def execute(
        self, keyspaces, unknown_keyspaces: List, user_id: UUID, steps_name: str
    ):
        step = self.initialize_step(user_id, steps_name)
        status = StepStatus.SUCCESS
        for keyspace, value in zip(unknown_keyspaces, keyspaces):
            if value < 0:
                logger.info(f"Skipping {keyspace}")
                status = StepStatus.FAILED
                continue
            self.process_keyspace(keyspace, value)
        step.status = status.value

    def initialize_step(self, user_id: UUID, steps_name: str) -> Step:
        step = self._dbh.get_steps(user_id, steps_name)
        step.status = StepStatus.PROCESSING.value
        return step

    def process_keyspace(self, keyspace, value):
        keyspace["value"] = value
        keyspace_schema = get_keyspace_adapter().validate_python(keyspace)

        def callback(keyspace_model):
            self._session.add(keyspace_model)

        visitor = KeyspaceModelCreator(callback, {})
        keyspace_schema.accept(visitor)
