import logging

from aiogram.types import Message
from aiogram.types.input_file import BufferedInputFile

from commands import BaseCommand
from config.uuid import UUIDGenerator
from dec import register_command
from schemas import CeleryResponse
from state import MessageWrapper

logger = logging.getLogger(__name__)


@register_command
class PubKey(BaseCommand):
    @property
    def command(self):
        return "pubkey"

    @property
    def description(self):
        return "Get my public GPG key"

    async def handle(self, message: Message | MessageWrapper):
        if self._is_document_message(message):
            await self._add_user_pubkey(message)
        else:
            await self._get_pubkey(message)

    async def _add_user_pubkey(self, message: Message | MessageWrapper):
        userid = UUIDGenerator.generate(str(message.from_user.id))
        document_id = message.document.file_id
        file_info = await self.bot.get_file(document_id)
        file_bytes = await self.bot.download_file(file_info.file_path)
        pubkey = file_bytes.read().decode("UTF-8")

        task = self.app.send_task("server.upload_user_pubkey", args=(userid, pubkey))
        result = CeleryResponse(**task.get(timeout=60))
        await self._process_celery_response(message, result)

    async def _get_pubkey(self, message: Message | MessageWrapper):
        result = self.app.send_task("server.get_pubkey")
        processing_result = CeleryResponse(**result.get(timeout=60))

        async def send_message(message: Message | MessageWrapper, value: bytes):
            document = BufferedInputFile(value, filename="pubkey.asc")
            await message.answer_document(document=document)

        await self._process_celery_response(message, processing_result, send_message)

