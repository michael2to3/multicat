from aiogram.types import Message, ContentType
from commands import BaseCommand
from .register_command import register_command


@register_command
class ListSteps(BaseCommand):
    @property
    def command(self):
        return "liststeps"

    @property
    def description(self):
        return "View avaliable steps for hashcat"

    async def handle(self, message: Message):
        result = self.app.send_task("main.liststeps", queue="server")
        processing_result = result.get(timeout=10)
        await message.answer(f"{processing_result}")
