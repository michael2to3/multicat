import logging
import uuid
from config import CeleryApp
from config import CeleryApp
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from models import HashcatAsset
from config import Config

app = CeleryApp("server").get_app()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

engine = create_async_engine(Config.get("DATABASE_URL"), echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def fetch_assets_by_uuid(task_uuid):
    async with SessionLocal() as session:
        async with session.begin():
            result = await session.execute(
                select(HashcatAsset).where(HashcatAsset.task_uuid == task_uuid)
            )
            return result.scalars().all()


@app.task()
def collect_wordlists():
    task_uuid = uuid.uuid4()
    task = app.send_task(
        "b.get_wordlists",
        args=(str(task_uuid),),
        queue="broadcast",
    )
    task.get()
    assets = asyncio.run(fetch_assets_by_uuid(task_uuid))
    return [asset.to_dict() for asset in assets]


@app.task
def get_rules():
    result = app.send_task("main.get_rules", queue="client")
    return result
