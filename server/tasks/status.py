import logging
from datetime import datetime
from typing import cast
from uuid import UUID
from zoneinfo import ZoneInfo

from celery import shared_task

from config import Database
from dec import init_user
from models.hashcat_request import Job, JobStatus
from schemas import CeleryResponse, JobProgress

db = Database()
logger = logging.getLogger(__name__)


def create_job_progress(job: Job) -> JobProgress:
    job_status = cast(str, job.status)
    status = (
        JobStatus[job_status]
        if job_status in JobStatus.__members__
        else JobStatus.FAILED
    )
    return JobProgress(
        id=cast(UUID, job.id),
        progress=42,
        status=status,
        start_at=datetime.min.replace(tzinfo=ZoneInfo("UTC")),
        end_at=datetime.min.replace(tzinfo=ZoneInfo("UTC")),
    )


@shared_task(name="server.get_status_by_jobid")
@init_user(db.session)
def get_status_by_jobid(owner_id: UUID, job_id: UUID):
    with db.session() as session:
        job = session.query(Job).filter(Job.id == job_id).first()
        if job is None:
            return CeleryResponse(
                error="Job not found", warning="", value=None
            ).model_dump()

        job_progress = create_job_progress(job)
        return CeleryResponse(value=job_progress, error="", warning="").model_dump()


@shared_task(name="server.get_status_by_userid")
@init_user(db.session)
def get_status_by_userid(owner_id: UUID):
    with db.session() as session:
        jobs = session.query(Job).filter(Job.user_id == owner_id).all()
        job_progresses = [create_job_progress(job) for job in jobs]
        return CeleryResponse(value=job_progresses, error="", warning="").model_dump()
