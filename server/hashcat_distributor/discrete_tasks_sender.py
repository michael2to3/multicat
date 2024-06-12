from logging import getLogger
from typing import Iterable, cast
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import scoped_session

import models
from db import DatabaseHelper

logger = getLogger(__name__)


class BruteforceConfigurationManager:
    _owner_id: UUID
    _step_name: str
    _hashtype: models.HashType
    _hashes: list[str]
    _session: scoped_session
    _dbh: DatabaseHelper

    def __init__(
        self,
        owner_id: UUID,
        step_name: str,
        hashtype: models.HashType,
        hashes: list[str],
        session: scoped_session,
    ):
        self._owner_id = owner_id
        self._step_name = step_name
        self._hashtype = hashtype
        self._hashes = hashes
        self._session = session
        self._dbh = DatabaseHelper(self._session)

    def get_new_configuration(
        self,
    ) -> models.Job:

        hashes = self._get_missing_or_uncracked_hashes()
        job = self._create_job()
        self._bind_job_to_hashes(job, hashes)

        self._upload_job_configuration(job, [cast(str, i.value) for i in hashes])

        return job

    def _create_job(self) -> models.Job:
        user: models.User = self._dbh.get_or_create_user(self._owner_id)
        job = models.Job(owning_user=user)
        return job

    def _get_missing_or_uncracked_hashes(self) -> list[models.Hash]:
        exist_hashes = (
            self._session.query(models.Hash)
            .filter(
                models.Hash.hash_type == self._hashtype,
                models.Hash.value.in_(self._hashes),
            )
            .all()
        )
        exist_hashes_value = {cast(str, h.value) for h in exist_hashes}
        non_exist_hashes = set(self._hashes) - exist_hashes_value

        new_hashes = [
            models.Hash(hash_type=self._hashtype, value=hash_value, is_cracked=False)
            for hash_value in non_exist_hashes
        ]
        if new_hashes:
            try:
                self._session.bulk_save_objects(new_hashes)
                self._session.commit()
            except IntegrityError:
                self._session.rollback()

        non_cracked_hashes = [h for h in exist_hashes if cast(bool, h.is_cracked)]

        return new_hashes + non_cracked_hashes

    def _bind_job_to_hashes(self, job: models.Job, hash_set: list[models.Hash]):
        for hash_obj in hash_set:
            hash_obj.related_jobs.append(job)

    def _upload_job_configuration(self, job: models.Job, new_hashes: Iterable[str]):
        new_hash_objects = [
            models.Hash(hash_type=self._hashtype, related_jobs=[job], value=hash_value)
            for hash_value in new_hashes
        ]
        self._session.add_all(new_hash_objects)
        self._session.add(job)
        self._session.flush()
