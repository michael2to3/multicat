from aiogram.types import Message
from commands import BaseCommand
from schemas import CeleryResponse

from .register_command import register_command


@register_command
class Devices(BaseCommand):
    @property
    def command(self):
        return "devices"

    @property
    def description(self):
        return "Get devices info from workers"

    async def _process_celery_response(self, message: Message, response):
        celery_response = CeleryResponse(**response.get(timeout=10))

        if celery_response.error:
            await message.answer(f"Error: {celery_response.error}")
        elif celery_response.warning:
            await message.answer(f"Warning: {celery_response.warning}")
        elif celery_response.value:
            await message.answer(f"{celery_response.value}")
        else:
            await message.answer("Operation completed successfully.")

    async def handle(self, message: Message):
        result = self.app.send_task("server.get_devices")
        await self._process_celery_response(message, result)
