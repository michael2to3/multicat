import logging
from aiogram.types import Message
from commands import BaseCommand
from schemas import CeleryResponse
from .register_command import register_command

logger = logging.getLogger(__name__)


@register_command
class ListSteps(BaseCommand):
    @property
    def command(self):
        return "liststeps"

    @property
    def description(self):
        return "List saved rules"

    async def handle(self, message: Message):
        userid = str(message.from_user.id)
        result = self.app.send_task(
            "main.liststeps", args=(userid,), queue="server"
        )
        processing_result = result.get(timeout=10)
        celery_response = CeleryResponse(**processing_result)

        if celery_response.error:
            await message.answer(f"Error: {celery_response.error}")
        else:
            message_text = "Your saved rules:\n"
            if celery_response.value:
                steps_list = "\n".join(
                    f"- {step}" for step in map(str, celery_response.value)
                )
                message_text += f"{steps_list}\n"
            if celery_response.warning:
                message_text += f"\nWarning: {celery_response.warning}"
            message_text += "You can download rule with command /getsteps NAME"
            await message.answer(message_text)
