from pydantic import BaseModel
from typing import List, Union
from aiogram.types import Message, ContentType
from commands import BaseCommand
from .register_command import register_command


@register_command
class Hashcat(BaseCommand):
    @property
    def command(self):
        return "hashcat"

    @property
    def description(self):
        return "Start attack!!1!1!11"

    async def handle(self, message: Message):
        if message.content_type == ContentType.DOCUMENT:
            document_id = message.document.file_id
            file_info = await self.bot.get_file(document_id)
            file_path = file_info.file_path
            file = await self.bot.download_file(file_path)

            result = self.app.send_task(
                "main.run_hashcat", args=(file), queue="server"
            )
            processing_result = result.get(timeout=10)
            await message.answer(f"{processing_result}")
        else:
            await message.answer("Please send a GPG-encrypted YAML file.")
