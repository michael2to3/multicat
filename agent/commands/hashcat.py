from aiogram.types import Message, ContentType
from commands import BaseCommand
from schemas import CeleryResponse
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
            message_text = message.caption
            if not message_text:
                await message.answer(
                    "Text is empty. Please send command with hashtype and namerule.\nExample: /hashcat HASHTYPE NAMERULE"
                )
                return
            parts = message_text.split(" ")
            if len(parts) != 3:
                await message.answer(
                    "Invalid command. Please send command with hashtype and namerule.\nExample: /hashcat HASHTYPE NAMERULE"
                )
                return

            hashtype, namerule = parts[1], parts[2]
            file_info = await self.bot.get_file(document_id)
            file_path = file_info.file_path
            file = await self.bot.download_file(file_path)
            content = file.read()

            result = self.app.send_task(
                "main.hashcat_run",
                args=(hashtype, namerule, content.decode("UTF-8")),
                queue="server",
            )

            resp = CeleryResponse(**result.get(timeout=10))

            message_response = "" if resp.value is None else resp.value
            if resp.error:
                message_response += f"\nError: {resp.error}"
            if resp.warning:
                message_response += f"\nWarning: {resp.warning}"

            await message.answer(message_response)
        else:
            await message.answer("Please send a GPG-encrypted YAML file.")
