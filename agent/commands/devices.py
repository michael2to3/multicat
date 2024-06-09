from aiogram.types import Message

from commands import BaseCommand
from dec import register_command
from schemas import CeleryResponse
from state import MessageWrapper


@register_command
class Devices(BaseCommand):
    @property
    def command(self):
        return "devices"

    @property
    def description(self):
        return "Get devices info from workers"

    async def handle(self, message: Message | MessageWrapper):
        result = self.app.send_task("server.get_devices")
        celery_response = CeleryResponse(**result.get(timeout=10))
        await self._process_celery_response(message, celery_response)
