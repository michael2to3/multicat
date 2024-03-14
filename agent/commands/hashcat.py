import gnupg
from pydantic import BaseModel, Field, validator, ValidationError, parse_obj_as
from typing import List, Union
import yaml
from aiogram.types import Message, ContentType
from commands import BaseCommand
from .register_command import register_command
from schemas import hashcat_step_constructor, Steps


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

            gpg = gnupg.GPG()
            decrypted_data = gpg.decrypt_file(file)

            if not decrypted_data.ok:
                await message.answer("Failed to decrypt the file.")
                return

            yaml.SafeLoader.add_constructor("!hashcatstep", hashcat_step_constructor)

            yaml_data = yaml.safe_load(decrypted_data.data)

            try:
                yaml_data = yaml.safe_load(decrypted_data.data)
                yaml_model = parse_obj_as(Steps, {"steps": yaml_data})
            except yaml.YAMLError as ye:
                await message.answer(f"Failed to load YAML content: {str(ye)}")
                return
            except ValidationError as ve:
                await message.answer(
                    f"Validation error for the provided data: {str(ve)}"
                )
                return

            task_data = yaml_model.json()

            result = self.app.send_task(
                "main.run_hashcat", args=(task_data,), queue="server"
            )
            processing_result = result.get(timeout=10)
            await message.answer(f"{processing_result}")
        else:
            await message.answer("Please send a GPG-encrypted YAML file.")
