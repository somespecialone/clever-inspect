import json
import warnings

from app.core.config import settings
from app.services import inspect_pool, InspectBot


async def pool_startup():
    # omit warning
    warnings.filterwarnings("ignore", category=UserWarning)

    with settings.CRED_FILE.open("r") as file:
        bots_data: list[dict] = json.load(file)

    for bot_data in bots_data:
        bot_data["id"] = bot_data.pop("steam_id")
        inspect_pool.add(InspectBot(**bot_data))

    if bots_data:
        await inspect_pool.startup()
    else:
        raise KeyboardInterrupt  # shut app off


async def pool_shutdown():
    await inspect_pool.shutdown()
