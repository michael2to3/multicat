import json
from typing import Dict, List, cast
from uuid import UUID

from sqlalchemy.orm import Query

import models
import schemas
from exc.steps import StepNotFoundError
from models import Step, User, UserRole
from visitor import KeyspaceModelQueryExecutor


class DatabaseHelperNotFoundError(Exception):
    pass


class DatabaseHelper:
    def __init__(self, session):
        self.session = session

    def get_or_create_hashtype_as_schema(self, identifier: str) -> schemas.HashType:
        hashtype = self.get_or_create_hashtype_as_model(identifier)
        return schemas.HashType(
            hashcat_type=cast(int, hashtype.hashcat_type),
            human_readable=cast(str, hashtype.human_readable),
        )

    def get_or_create_hashtype_as_model(self, identifier: str) -> models.HashType:
        identifier_normalized = identifier.lower().strip()
        hashtype = self._get_hashtype(identifier_normalized)
        if hashtype is None and identifier_normalized.isdigit():
            hashtype = self._create_unnamed_hashtype(int(identifier_normalized))

        if hashtype is None:
            raise DatabaseHelperNotFoundError(f"Hash type '{identifier}' not found")

        return hashtype

    def _get_hashtype(self, identifier: str) -> models.HashType:
        if identifier.isdigit():
            return (
                self.session.query(models.HashType)
                .filter(models.HashType.hashcat_type == int(identifier))
                .first()
            )
        else:
            return (
                self.session.query(models.HashType)
                .filter(models.HashType.human_readable == identifier)
                .first()
            )

    def _create_unnamed_hashtype(self, hashcat_type: int) -> models.HashType:
        hashtype = models.HashType(human_readable="unnamed", hashcat_type=hashcat_type)
        self.session.add(hashtype)
        self.session.flush()
        return hashtype

    def _convert_to_schema_hashtype(
        self, hashtype: models.HashType
    ) -> schemas.HashType:
        return schemas.HashType(
            hashcat_type=cast(int, hashtype.hashcat_type),
            human_readable=cast(str, hashtype.human_readable),
        )

    def get_or_create_user(self, user_id: UUID) -> User:
        user = self.session.query(User).filter(User.id == user_id).first()
        if not user:
            user = User(id=user_id, role=UserRole.USER.value)
            self.session.add(user)
            self.session.flush()
        return user

    def get_unique_name_hashcatrules(self, desired_name: str) -> str:
        counter = 1
        unique_name = desired_name
        existing_names = (
            self.session.query(Step.name)
            .filter(Step.name.like(f"{desired_name}%"))
            .all()
        )
        existing_names = set(name[0] for name in existing_names)

        while unique_name in existing_names:
            unique_name = f"{desired_name}{counter}"
            counter += 1

        return unique_name

    def get_steps(self, user_id: UUID, step_name: str) -> Step:
        step = (
            self.session.query(Step)
            .filter(Step.user_id == user_id, Step.name == step_name)
            .first()
        )
        if not step:
            raise StepNotFoundError("Loaded steps not found")

        return step

    def get_hashcat_steps(self, user_id: UUID, step_name: str) -> schemas.Steps:
        step = (
            self.session.query(Step)
            .filter(Step.user_id == user_id, Step.name == step_name)
            .first()
        )
        if not step:
            raise StepNotFoundError("Loaded steps not found")

        return self._convert_to_schema_steps(step)

    def _convert_to_schema_steps(self, step: Step) -> schemas.Steps:
        hashcat_steps = {"steps": [json.loads(s.value) for s in step.hashcat_steps]}
        return schemas.Steps(**hashcat_steps)

    def keyspace_exists(self, keyspace: schemas.KeyspaceBase) -> bool:
        callback_result = [False]

        def callback(query: Query):
            callback_result[0] = query.first() is not None

        visitor = KeyspaceModelQueryExecutor(
            self.session, callback, {"value", "attack_mode"}
        )
        keyspace.accept(visitor)
        return callback_result[0]

    def get_devices(self) -> List[models.Devices]:
        result = self.session.query(models.Devices).all()
        return result

    def get_worker_devices(self, worker_name: str) -> models.Devices:
        result = (
            self.session.query(models.Devices)
            .filter(models.Devices.worker_name == worker_name)
            .first()
        )
        return result

    def add_devices_info(self, worker_name: str, value: Dict) -> models.Devices:
        devices = models.Devices(worker_name=worker_name, value=value)
        self.session.add(devices)
        self.session.flush()
        return devices
