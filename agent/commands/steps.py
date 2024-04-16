import logging
from uuid import UUID

from aiogram.enums import ParseMode
from aiogram.types import ContentType, Message
from aiogram.types.input_file import BufferedInputFile

from commands import BaseCommand
from commands.message_wrapper import MessageWrapper
from config.uuid import UUIDGenerator
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
        return "Manage workflow steps with subcommands: /steps list (view all steps), /steps get (details of a step), /steps load (add/update steps via YAML file), /steps delete (remove a step), /steps original (view original step), /steps print (print steps)"

    async def handle(self, message: Message | MessageWrapper):
        subcommand = self._parse_command(message)
        userid = UUIDGenerator.generate(str(message.from_user.id))
        match subcommand:
            case "list" | "l":
                return await self._handle_list(userid, message)
            case "get" | "g":
                return await self._handle_get(userid, message)
            case "original" | "o":
                return await self._handle_orig(userid, message)
            case "print" | "p":
                return await self._handle_print_orig(userid, message)
            case "load" | "lo":
                return await self._handle_load(userid, message)
            case "delete" | "d":
                return await self._handle_delete(userid, message)
            case _:
                await self._process_unknown_subcommand(message, subcommand)

    async def _process_unknown_subcommand(
        self, message: Message | MessageWrapper, subcommand: str
    ):
        text = (
            "Unknown subcommand. Available subcommands: list, get, original, load, delete, print"
            if subcommand
            else "You can use subcommands: list, get, original, load, delete, print"
        )
        return await message.answer(text)

    def _get_message_text(self, message: Message | MessageWrapper) -> str:
        text = message.text if message.text else message.caption
        return text if text else ""

    def _parse_command(self, message: Message | MessageWrapper) -> str:
        message_text = self._get_message_text(message)
        if not message_text:
            return ""
        parts = message_text.split(" ", 2)
        if len(parts) > 1:
            return parts[1]
        return ""

    def _parse_text(self, message: Message | MessageWrapper) -> str:
        message_text = self._get_message_text(message)
        if not message_text:
            return ""
        parts = message_text.split(" ", 2)
        if len(parts) > 2:
            return parts[2]
        return ""

    async def _process_celery_response(
        self, message: Message | MessageWrapper, response
    ):
        celery_response = CeleryResponse(**response.get(timeout=10))

        if celery_response.error:
            await message.answer(f"Error: {celery_response.error}")
        elif celery_response.warning:
            await message.answer(f"Warning: {celery_response.warning}")
        elif celery_response.value:
            await message.answer(f"{celery_response.value}")
        else:
            await message.answer("Operation completed successfully.")

    async def _handle_list(self, userid: UUID, message: Message | MessageWrapper):
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

    async def _common_handle(
        self, userid: UUID, message: Message | MessageWrapper, task: str
    ):
        step_name = self._parse_text(message)
        if not step_name:
            await message.answer("Please enter step name")
            return

        result = self.app.send_task(task, args=(userid, step_name))
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

    async def _handle_get(self, userid: UUID, message: Message | MessageWrapper):
        await self._common_handle(userid, message, "server.get_steps")

    async def _handle_orig(self, userid: UUID, message: Message | MessageWrapper):
        await self._common_handle(userid, message, "server.get_orig_steps")

    async def _handle_print_orig(self, userid: UUID, message: Message | MessageWrapper):
        step_name = self._parse_text(message)
        if not step_name:
            await message.answer("Please enter step name")
            return

        result = self.app.send_task("server.get_orig_steps", args=(userid, step_name))
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
        await message.answer(f"```{step_details}```", parse_mode=ParseMode.MARKDOWN_V2)

    async def _handle_load(self, userid: UUID, message: Message | MessageWrapper):
        if message.content_type != ContentType.DOCUMENT:
            await message.answer("Please send a YAML file.")
            return

        document_id, file_name = message.document.file_id, message.document.file_name
        file_info = await self.bot.get_file(document_id)
        file_bytes = await self.bot.download_file(file_info.file_path)
        content = file_bytes.read().decode("UTF-8")

        result = self.app.send_task(
            "server.load_steps", args=(userid, file_name, content)
        )
        await self._process_celery_response(message, result)

    async def _handle_delete(self, userid: UUID, message: Message | MessageWrapper):
        text_message = self._parse_text(message)
        if not text_message:
            await message.answer("Please enter step name")
            return

        result = self.app.send_task("server.delete_steps", args=(userid, text_message))
        await self._process_celery_response(message, result)
