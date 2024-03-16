import logging
from typing import List, Dict
from schemas import CeleryResponse, HashcatAssetSchema
from aiogram.types import Message
from .command import BaseCommand
from .register_command import register_command

logger = logging.getLogger(__name__)


@register_command
class Assets(BaseCommand):
    @property
    def command(self):
        return "assets"

    @property
    def description(self):
        return "Get assets for hashcat"

    async def handle(self, message: Message):
        try:
            if message.from_user is None:
                await message.answer("Please use this command in private")
                return

            userid = str(message.from_user.id)
            task = self.app.send_task(
                "main.collect_assets", args=(userid,), queue="server"
            )
            resp = CeleryResponse(**task.get(timeout=10))

            if resp.error:
                await message.answer(f"Error: {resp.error}")
                return
            if resp.warning:
                await message.answer(f"Warning: {resp.warning}")

            assets_schemas: List[HashcatAssetSchema] = [
                HashcatAssetSchema(**asset) for asset in resp.value
            ]
            assets_by_worker: Dict[str, Dict[str, List[str]]] = {}
            for asset in assets_schemas:
                if asset.worker_id not in assets_by_worker:
                    assets_by_worker[asset.worker_id] = {"wordlists": [], "rules": []}
                assets_by_worker[asset.worker_id]["wordlists"].extend(
                    asset.wordlists or ["empty wordlist"]
                )
                assets_by_worker[asset.worker_id]["rules"].extend(
                    asset.rules or ["empty rule"]
                )

            message_text = ""
            for worker_id, assets in assets_by_worker.items():
                wordlists_text = "\n".join(
                    f"- {wordlist}" for wordlist in assets["wordlists"]
                )
                rules_text = "\n".join(f"- {rule}" for rule in assets["rules"])
                worker_assets_text = (
                    f"{worker_id}:\nWordlists:\n{wordlists_text}\nRules:\n{rules_text}"
                )
                message_text += worker_assets_text + "\n\n"

            await message.answer(
                message_text.strip() if message_text else "No assets found."
            )
        except Exception as e:
            logger.error(f"Failed to process assets command: %s", e)
            await message.answer("Failed to process your request.")
