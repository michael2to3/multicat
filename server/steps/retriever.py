import json
import logging
from uuid import UUID

import yaml
from sqlalchemy.orm import scoped_session

from db import DatabaseHelper
from models import Step

logger = logging.getLogger(__name__)


class StepRetriever:
    def __init__(self, user_id: UUID, session: scoped_session):
        self._dbh = DatabaseHelper(session)
        self._session = session
        self._user_id = user_id

    def get_steps(self, step_name: str):
        user = self._dbh.get_or_create_user(self._user_id)
        step = self._get_step_with_keyspace(user.id, step_name)
        if not step:
            raise ValueError("Step not found.")
        hashcat_steps = [json.loads(s.value) for s in step.hashcat_steps]
        return yaml.dump(hashcat_steps, default_flow_style=False, allow_unicode=True)

    def list_steps(self):
        user = self._dbh.get_or_create_user(self._user_id)
        steps = self._session.query(Step.name).filter(Step.user_id == user.id).all()
        return [step.name for step in steps] if steps else []

    def _get_step_with_keyspace(self, user_id, step_name):
        return (
            self._session.query(Step)
            .filter(
                Step.user_id == user_id,
                Step.name == step_name,
                Step.is_keyspace_calculated,
            )
            .first()
        )
