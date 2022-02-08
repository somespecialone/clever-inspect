from .pool import InspectPool, InspectBot

from .game_data import GameData
from app.core.config import settings

__all__ = ("inspect_pool", "game_data", "InspectBot")

inspect_pool = InspectPool()
inspect_pool.randomizer = settings.UPDATE_INTERVAL
inspect_pool.INSPECT_TIMEOUT = settings.INSPECT_TIMEOUT

game_data = GameData(settings.SCHEMAS_DIR_URL)
