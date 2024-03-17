import logging
from aiogram.types import Message, ContentType
from commands import BaseCommand
from schemas import CeleryResponse
from .register_command import register_command

logger = logging.getLogger(__name__)


@register_command
class LoadSteps(BaseCommand):
    @property
    def command(self):
        return "loadsteps"

    @property
    def description(self):
        return "Load Steps for hashcat"

    async def handle(self, message: Message):
        if message.content_type != ContentType.DOCUMENT:
            await message.answer("Please send a YAML file.")
            return

        userid = str(message.from_user.id)
        document_id = message.document.file_id
        file_name = message.document.file_name
        file_info = await self.bot.get_file(document_id)
        file_path = file_info.file_path
        file_bytes = await self.bot.download_file(file_path)
        content = file_bytes.read()

        result = self.app.send_task(
            "main.loadsteps",
            args=(userid, file_name, content.decode("UTF-8")),
            queue="server",
        )
        processing_result = CeleryResponse(**result.get(timeout=10))

        response_message = ""
        if processing_result.error:
            response_message = f"Error: {processing_result.error}"
        else:
            if processing_result.warning:
                response_message += f"Warning: {processing_result.warning}\n"
            if processing_result.value:
                response_message += str(processing_result.value)

        await message.answer(
            response_message if response_message else "Step loaded successfully."
        )
