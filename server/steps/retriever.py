import json
import logging

import yaml
from sqlalchemy.orm import scoped_session

from db import DatabaseHelper
from models import Step

logger = logging.getLogger(__name__)


class StepRetriever:
    def __init__(self, user_id: str, session: scoped_session):
        self.db_helper = DatabaseHelper(session)
        self.session = session
        self.user_id = user_id

    def get_steps(self, step_name: str):
        user = self.db_helper.get_or_create_user(self.user_id)
        step = self._get_step_with_keyspace(user.id, step_name)
        if not step:
            raise ValueError("Step not found.")
        hashcat_steps = [json.loads(s.value) for s in step.hashcat_steps]
        return yaml.dump(hashcat_steps, default_flow_style=False, allow_unicode=True)

    def list_steps(self):
        user = self.db_helper.get_or_create_user(self.user_id)
        steps = self.session.query(Step.name).filter(Step.user_id == user.id).all()
        return [step.name for step in steps] if steps else []

    def _get_step_with_keyspace(self, user_id, step_name):
        return (
            self.session.query(Step)
            .filter(
                Step.user_id == user_id,
                Step.name == step_name,
                Step.is_keyspace_calculated,
            )
            .first()
        )
