import logging
from aiogram.types import Message
from aiogram.types.input_file import BufferedInputFile
from commands import BaseCommand
from .register_command import register_command
from schemas import CeleryResponse

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

        try:
            result = self.app.send_task(
                "main.getsteps", args=(userid, text_message), queue="server"
            )
            processing_result_raw = result.get(timeout=10)
            resp = CeleryResponse(**processing_result_raw)

            message_response = "" if resp.value is None else resp.value
            if resp.error:
                message_response += f"\nError: {resp.error}"
            if resp.warning:
                message_response += f"\nWarning: {resp.warning}"
            if resp.value:
                document = BufferedInputFile(resp.value, filename=text_message)
                await message.answer_document(
                    document=document, caption=message_response
                )
            else:
                await message.answer(message_response)
        except Exception as e:
            logger.error("Failed to process getsteps: %s", e)
            await message.answer("Failed to process your request.")
