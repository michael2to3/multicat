import logging
from aiogram.types import Message
from commands import BaseCommand
from .register_command import register_command
from schemas import CeleryResponse

logger = logging.getLogger(__name__)


@register_command
class DelSteps(BaseCommand):
    @property
    def command(self):
        return "delsteps"

    @property
    def description(self):
        return "Delete Steps for hashcat"

    async def handle(self, message: Message):
        userid = str(message.from_user.id)
        text_message = " ".join(message.text.split(" ")[1:])
        if not text_message:
            await message.answer("Please enter step name")
            return

        try:
            result = self.app.send_task(
                "main.delsteps", args=(userid, text_message), queue="server"
            )
            celery_response = CeleryResponse(**result.get(timeout=10))

            if celery_response.error:
                await message.answer(f"Error: {celery_response.error}")
            elif celery_response.warning:
                await message.answer(f"Warning: {celery_response.warning}")
            elif celery_response.value:
                await message.answer(f"{celery_response.value}")
            else:
                await message.answer(
                    "Operation completed with no additional information."
                )
        except Exception as e:
            logger.error("Failed to process delsteps: %s", e)
            await message.answer("Failed to process your request.")
