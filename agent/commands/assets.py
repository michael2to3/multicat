import asyncio
from typing import List
from celery.result import AsyncResult
from aiogram.types import Message
from .command import BaseCommand
from .register_command import register_command
from schemas import HashcatAssetSchema


@register_command
class Assets(BaseCommand):
    @property
    def command(self):
        return "assets"

    @property
    def description(self):
        return "Get a list of wordlists/rules"

    async def handle(self, message: Message):
        userid = str(message.from_user.id)
        task = self.app.send_task("main.collect_assets", args=(userid,), queue="server")
        assets = task.get(timeout=10)
        assets_schemas: List[HashcatAssetSchema] = [
            HashcatAssetSchema(**asset) for asset in assets
        ]

        assets_by_worker = {}
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

        await message.answer(message_text.strip() if message_text else "Wait...")
