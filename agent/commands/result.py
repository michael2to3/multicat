import logging
from uuid import UUID

from aiogram.types import Message
from aiogram.types.input_file import BufferedInputFile

from commands import BaseCommand
from config.uuid import UUIDGenerator
from dec import register_command
from schemas import CeleryResponse
from state import MessageWrapper

logger = logging.getLogger(__name__)


@register_command
class Result(BaseCommand):
    @property
    def command(self):
        return "result"

    @property
    def description(self):
        return "Get result"

    async def handle(self, message: Message | MessageWrapper):
        userid = UUIDGenerator.generate(str(message.from_user.id))
        if message.text is None or len(message.text.split(" ")) != 2:
            await message.answer("Usage: /result <job_id>")
            return

        jobid = UUID(message.text.split(" ")[1].strip())
        result = self.app.send_task("server.get_result", args=(userid, jobid))
        processing_result = CeleryResponse(**result.get(timeout=60))

        async def send_message(message: Message | MessageWrapper, value: str):
            document = BufferedInputFile(value.encode("utf-8"), filename="cracked_hashes.txt.gpg")
            await message.answer_document(document=document)

        await self._process_celery_response(
            message, processing_result, send_response=send_message
        )
