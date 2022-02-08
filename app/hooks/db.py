from ..db import engine, BaseModel
from ..models import *


async def db_startup():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


async def db_shutdown():
    await engine.dispose()
