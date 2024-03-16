import logging
from aiogram.types import Message
from aiogram.types.input_file import BufferedInputFile
from commands import BaseCommand
from schemas import CeleryResponse
from .register_command import register_command

logger = logging.getLogger(__name__)


@register_command
class PubKey(BaseCommand):
    @property
    def command(self):
        return "pubkey"

    @property
    def description(self):
        return "Get my public GPG key"

    async def handle(self, message: Message):
        result = self.app.send_task("main.get_pubkey", queue="server")
        processing_result = CeleryResponse(**result.get(timeout=60))

        if processing_result.error:
            await message.answer(f"Error: {processing_result.error}")
        else:
            if processing_result.warning:
                await message.answer(f"Warning: {processing_result.warning}")
            if processing_result.value:
                document = BufferedInputFile(
                    processing_result.value, filename="public_key.asc"
                )
                await message.answer_document(document=document)
            else:
                await message.answer("Couldn't find my public GPG key.")
