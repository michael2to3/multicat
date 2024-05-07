from typing import Iterable, List, Set
from uuid import UUID

from celery import chord, signature
from schemas.hashcat_helpers import hashcat_step_loader
from sqlalchemy.orm import scoped_session
from sqlalchemy import func, and_

import models
import schemas
from db import DatabaseHelper
from steps.loader import KeyspaceCalculator
from steps.retriever import StepRetriever


class BruteforceConfigurationManager:
    _owner_id: UUID
    _step_name: str
    _hashtype: str
    _hashes: List[str]
    _session: scoped_session

    def __init__(
        self,
        owner_id: UUID,
        step_name: str,
        hashtype: str,
        hashes: List[str],
        session: scoped_session,
    ):
        self._owner_id = owner_id
        self._step_name = step_name
        self._hashtype = hashtype
        self._hashes = hashes
        self._session = session
        self._db_helper = DatabaseHelper(self._session)

    def _load_steps(self) -> schemas.Steps:
        manager = StepRetriever(self._owner_id, self._session)
        yaml_content = manager.get_orig_steps(self._step_name)
        data = hashcat_step_loader().load(yaml_content)
        steps = schemas.Steps(**data)
        return steps

    def _get_hash_type(self) -> models.HashType:
        hash_type: schemas.HashType = self._db_helper.get_or_create_hashtype_as_schema(
            self._hashtype
        )
        self._session.commit()
        return hash_type

    def _get_job(self) -> models.Job:
        user: models.User = self._db_helper.get_or_create_user(self._owner_id)
        job = models.Job(owning_user=user)
        return job

    def _get_existing_hashes_set(self, hash_type) -> Set[str]:
        existing_hashes: List[models.Hash] = (
            self._session.query(models.Hash)
            .filter(
                models.Hash.hash_type == hash_type, models.Hash.value.in_(self._hashes)
            )
            .all()
        )
        existing_set = set(hash.value for hash in existing_hashes)
        return existing_set

    def _bind_job_to_hashes(self, job: models.Job, hash_set: Iterable[str]):
        for hash_obj in (
            self._session.query(models.Hash)
            .filter(models.Hash.value.in_(hash_set))
            .all()
        ):
            hash_obj.related_jobs.append(job)

    def _upload_job_configuration(
        self, job: models.Job, hash_type: models.HashType, new_hashes: Iterable[str]
    ):
        new_hash_objects = [
            models.Hash(hash_type=hash_type, related_jobs=[job], value=hash_value)
            for hash_value in new_hashes
        ]
        self._session.add_all(new_hash_objects)
        self._session.add(job)
        self._session.flush()

    def get_new_configuration(
        self,
    ) -> tuple[schemas.Steps, models.Job, models.HashType]:
        steps = self._load_steps()
        hash_type = self._get_hash_type()
        job = self._get_job()
        existing_set = self._get_existing_hashes_set(hash_type)

        self._bind_job_to_hashes(job, existing_set)
        new_hashes = [hash for hash in self._hashes if hash not in existing_set]
        self._upload_job_configuration(job, hash_type, new_hashes)

        return steps, job, hash_type
