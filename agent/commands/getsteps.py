import logging

from aiogram.types import Message
from aiogram.types.input_file import BufferedInputFile
from commands import BaseCommand
from schemas import CeleryResponse

from .register_command import register_command

logger = logging.getLogger(__name__)


@register_command
class GetSteps(BaseCommand):
    @property
    def command(self):
        return "getsteps"

    @property
    def description(self):
        return "Download Steps for hashcat"

    async def handle(self, message: Message):
        userid = str(message.from_user.id)
        text_message = " ".join(message.text.split(" ")[1:])
        if not text_message:
            await message.answer("Please enter step name")
            return

        result = self.app.send_task(
            "main.get_steps", args=(userid, text_message), queue="server"
        )
        processing_result_raw = result.get(timeout=10)
        resp = CeleryResponse(**processing_result_raw)

        if resp.error:
            await message.answer(f"Error: {resp.error}")
            return
        message_response = resp.warning if resp.warning else ""
        if resp.value:
            document = BufferedInputFile(
                bytes(resp.value, encoding="UTF-8"), filename=text_message
            )
            await message.answer_document(document=document, caption=message_response)
        else:
            await message.answer(message_response)
