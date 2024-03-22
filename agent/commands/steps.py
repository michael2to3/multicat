import logging

from aiogram.types import ContentType, Message
from aiogram.types.input_file import BufferedInputFile
from commands import BaseCommand
from schemas import CeleryResponse

from .register_command import register_command

logger = logging.getLogger(__name__)


@register_command
class Steps(BaseCommand):
    @property
    def command(self):
        return "steps"

    @property
    def description(self):
        return "Manage workflow steps with subcommands: /steps list (view all steps), /steps get (details of a step), /steps load (add/update steps via YAML file), /steps delete (remove a step)."

    async def handle(self, message: Message):
        subcommand = self._parse_command(message)
        match subcommand:
            case "list":
                return await self._handle_list(message)
            case "get":
                return await self._handle_get(message)
            case "load":
                return await self._handle_load(message)
            case "delete":
                return await self._handle_delete(message)
            case _:
                return await message.answer(f"Unknown subcommand: {subcommand}")

    def _get_message_text(self, message: Message) -> str:
        return message.text if message.text else message.caption

    def _parse_command(self, message: Message) -> str:
        message_text = self._get_message_text(message)
        if not message_text:
            return ""
        parts = message_text.split(" ", 2)
        if len(parts) > 1:
            return parts[1]
        return ""

    def _parse_text(self, message: Message) -> str:
        message_text = self._get_message_text(message)
        if not message_text:
            return ""
        parts = message_text.split(" ", 2)
        if len(parts) > 2:
            return parts[2]
        return ""

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

    async def _handle_list(self, message: Message):
        userid = str(message.from_user.id)
        result = self.app.send_task("server.list_steps", args=(userid,))
        celery_response = CeleryResponse(**result.get(timeout=10))

        if celery_response.error:
            return await message.answer(f"Error: {celery_response.error}")
        response_message = "Your steps:\n"
        if celery_response.value:
            steps_list = "\n".join(f"- {step}" for step in celery_response.value)
            response_message += f"{steps_list}\n"
        else:
            response_message += "No steps found."

        if celery_response.warning:
            response_message += f"\nWarning: {celery_response.warning}"

        return await message.answer(response_message)

    async def _handle_get(self, message: Message):
        userid, step_name = str(message.from_user.id), self._parse_text(message)
        if not step_name:
            await message.answer("Please enter step name")
            return

        result = self.app.send_task("server.get_steps", args=(userid, step_name))
        celery_response = CeleryResponse(**result.get(timeout=10))

        if celery_response.error:
            await message.answer(f"Error: {celery_response.error}")
            return
        if celery_response.warning:
            await message.answer(f"Warning: {celery_response.warning}")
        if not celery_response.value:
            await message.answer("Step not found.")
            return

        step_details = celery_response.value
        document = BufferedInputFile(
            bytes(step_details, encoding="UTF-8"), filename=step_name
        )
        await message.answer_document(
            document=document, caption=f"Details for step '{step_name}':"
        )

    async def _handle_load(self, message: Message):
        if message.content_type != ContentType.DOCUMENT:
            await message.answer("Please send a YAML file.")
            return

        userid = str(message.from_user.id)
        document_id, file_name = message.document.file_id, message.document.file_name
        file_info = await self.bot.get_file(document_id)
        file_bytes = await self.bot.download_file(file_info.file_path)
        content = file_bytes.read().decode("UTF-8")

        result = self.app.send_task(
            "server.load_steps", args=(userid, file_name, content)
        )
        await self._process_celery_response(message, result)

    async def _handle_delete(self, message: Message):
        userid, text_message = str(message.from_user.id), self._parse_text(message)
        if not text_message:
            await message.answer("Please enter step name")
            return

        result = self.app.send_task("server.delete_steps", args=(userid, text_message))
        await self._process_celery_response(message, result)
