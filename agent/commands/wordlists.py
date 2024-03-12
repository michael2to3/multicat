import asyncio
from typing import List
from celery.result import AsyncResult
from commands import BaseCommand
from aiogram.types import Message
from .register_command import register_command
from schemas import HashcatAssetSchema


@register_command
class Wordlists(BaseCommand):
    @property
    def command(self):
        return "wordlists"

    @property
    def description(self):
        return "Get wordlists from each client"

    async def handle(self, message: Message):
        userid = str(message.from_user.id)
        task = self.app.send_task(
            "main.collect_wordlists", args=(userid,), queue="server"
        )
        assets = task.get(timeout=10)
        assets_schemas: List[HashcatAssetSchema] = [
            HashcatAssetSchema(**asset) for asset in assets
        ]

        assets_by_worker = {}
        for asset in assets_schemas:
            if asset.worker_id not in assets_by_worker:
                assets_by_worker[asset.worker_id] = []
            assets_by_worker[asset.worker_id].extend(asset.wordlists or ["empty"])

        message_text = "\n".join(
            f"{worker_id}:\n" + "\n".join(f"- {wordlist}" for wordlist in wordlists)
            for worker_id, wordlists in assets_by_worker.items()
        )

        await message.answer(message_text if message_text else "Wait...")
