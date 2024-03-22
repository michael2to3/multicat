import base64

from aiogram.types import ContentType, Message

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

            user_id = str(message.from_user.id)
            hash_type, step_name = parts[1], parts[2]
            file_info = await self.bot.get_file(document_id)
            file_path = file_info.file_path
            file = await self.bot.download_file(file_path)
            content = base64.b64encode(file.read()).decode("utf-8")

            result = self.app.send_task(
                "server.run_hashcat",
                args=(user_id, hash_type, step_name, content),
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
