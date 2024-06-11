import logging
from uuid import UUID

from aiogram.types import Message

from config.uuid import UUIDGenerator
from dec import register_command
from schemas import JobProgress, JobStatus
from schemas.codegen.task_and_steps import CeleryResponse
from state import MessageWrapper, fetched

from .command import BaseCommand

logger = logging.getLogger(__name__)


@register_command
class Status(BaseCommand):
    @property
    def command(self) -> str:
        return "status"

    @property
    def description(self) -> str:
        return "Get status of the task"

    @fetched()
    async def handle(self, message: Message | MessageWrapper):
        if message.from_user is None:
            await message.answer("Please use this command in private")
            return

        userid = UUIDGenerator.generate(str(message.from_user.id))
        args = message.text.split() if message.text else []

        if len(args) == 2:
            await self._handle_specific_job(message, userid, UUID(args[1]))
        else:
            await self._handle_summary(message, userid)

    async def _handle_specific_job(
        self, message: Message | MessageWrapper, userid: UUID, jobid: UUID
    ):
        task = self.app.send_task("server.get_status_by_jobid", args=(userid, jobid))
        resp = CeleryResponse(**task.get(timeout=60))
        await self._process_celery_response(
            message, resp, send_response=self._format_detailed_job_progress
        )

    async def _handle_summary(self, message: Message | MessageWrapper, userid: UUID):
        task = self.app.send_task("server.get_status_by_userid", args=(userid,))
        resp = CeleryResponse(**task.get(timeout=60))
        await self._process_celery_response(
            message, resp, send_response=self._format_summary_response
        )

    async def _format_detailed_job_progress(
        self, message: Message | MessageWrapper, value: dict
    ):
        job_progress = JobProgress(**value)
        time_frame = f"{job_progress.start_at:%Y-%m-%d %H:%M} - {job_progress.end_at:%H:%M %Z}"
        progress_bar = self._create_progress_bar(job_progress.progress)
        resp_message = (
            f"{job_progress.id}  | {job_progress.status.value}\n"
            f"**Time:** {time_frame}\n"
            f"{job_progress.progress}% [{progress_bar}]\n"
            f"{self._status_specific_message(job_progress.status)}"
        )
        await message.answer(resp_message, parse_mode="Markdown")

    async def _format_summary_response(
        self, message: Message | MessageWrapper, value: list
    ):
        job_progress_list = [JobProgress(**jp) for jp in value]
        jobs_sorted = sorted(
            job_progress_list, key=lambda x: x.start_at, reverse=True
        )[:10]
        resp_message = "\n".join(self._format_job_summary(jp) for jp in jobs_sorted)
        await message.answer(resp_message, parse_mode="Markdown")

    def _format_job_summary(self, job_progress: JobProgress) -> str:
        progress_bar = self._create_progress_bar(job_progress.progress)
        return f"{job_progress.id} {job_progress.progress}% [{progress_bar}] {job_progress.status.value}"

    def _create_progress_bar(self, progress: int) -> str:
        total_bars = 20
        filled_bars = int(progress / 100 * total_bars)
        empty_bars = total_bars - filled_bars
        return "█" * filled_bars + "░" * empty_bars

    def _status_specific_message(self, status: JobStatus) -> str:
        messages = {
            JobStatus.COMPLETED: "✅ Completed.\n",
            JobStatus.RUNNING: "⏳ Running...\n",
            JobStatus.FAILED: "❌ Failed.\n",
            JobStatus.CREATED: "🚀 Ready to start.\n",
        }
        return messages.get(status, "")
