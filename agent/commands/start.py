from commands import BaseCommand
from aiogram.types import Message
from .register_command import register_command


@register_command
class Start(BaseCommand):
    @property
    def command(self):
        return "start"

    @property
    def description(self):
        return "Start the bot and get a welcome message"

    async def handle(self, message: Message):
        await message.answer(
            "Привет! Я Агент для отправки хешей на обработку. Отправь мне хеш для обработки."
        )
