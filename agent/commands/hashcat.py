import base64

from aiogram.types import Message

from commands import BaseCommand
from config.uuid import UUIDGenerator
from dec import register_command
from schemas import CeleryResponse
from state import MessageWrapper


@register_command
class Hashcat(BaseCommand):
    @property
    def command(self) -> str:
        return "hashcat"

    @property
    def description(self) -> str:
        return "Start attack!!1!1!11"

    async def handle(self, message: Message | MessageWrapper) -> None:
        if self._is_document_message(message):
            await self._handle_document(message)
        else:
            await message.answer("Please send a GPG-encrypted YAML file.")

    async def _handle_document(self, message: Message | MessageWrapper) -> None:
        if not message.caption:
            await message.answer(
                "Text is empty. Please send command with hashtype and namerule.\nExample: /hashcat HASHTYPE NAMERULE"
            )
            return

        parts = message.caption.split(" ")
        if len(parts) != 3:
            await message.answer(
                "Invalid command. Please send command with hashtype and namerule.\nExample: /hashcat HASHTYPE NAMERULE"
            )
            return

        user_id, hash_type, step_name = self._parse_command_parts(message, parts)
        file_info = await self.bot.get_file(message.document.file_id)

        if not file_info or not file_info.file_path:
            await message.reply("File not found.")
            return

        file_content = await self._download_and_encode_file(file_info.file_path)
        if file_content is None:
            await message.reply("Cannot download file.")
            return

        await self._send_task_and_respond(
            message, user_id, hash_type, step_name, file_content
        )

    def _parse_command_parts(
        self, message: Message | MessageWrapper, parts: list
    ) -> tuple:
        user_id = UUIDGenerator.generate(str(message.from_user.id))
        hash_type, step_name = parts[1], parts[2]
        return user_id, hash_type, step_name

    async def _download_and_encode_file(self, file_path: str) -> str | None:
        file = await self.bot.download_file(file_path)
        if file is None:
            return None
        return base64.b64encode(file.read()).decode("utf-8")

    async def _send_task_and_respond(
        self,
        message: Message | MessageWrapper,
        user_id: str,
        hash_type: str,
        step_name: str,
        content: str,
    ) -> None:
        result = self.app.send_task(
            "server.run_hashcat",
            args=(user_id, hash_type, step_name, content),
        )
        resp = CeleryResponse(**result.get(timeout=10))

        async def resp_message(message: Message | MessageWrapper, x: int):
            await message.answer(
                f"Hey there! Just kicked off your hashcat attack 🐱💻. Track it with `/status {x}` or peek at all ongoing shenanigans with `/status`.",
                parse_mode="Markdown",
            )

        await self._process_celery_response(message, resp, resp_message)
