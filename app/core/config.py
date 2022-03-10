from pathlib import Path
from typing import Callable, Any

from pydantic import BaseSettings, FilePath, AnyUrl, DirectoryPath
from steam_tradeoffer_manager import ONCE_EVERY


class AppSettings(BaseSettings):
    DEBUG: bool = False

    ROOT_DIR: DirectoryPath = Path(__file__).parent.parent.parent

    # meta
    PROJECT_TITLE: str = "Clever inspect"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "CSGO 🔫 items inspect service"

    PROJECT_TERMS_OF_SERVICE: AnyUrl = "https://github.com/somespecialone/clever-inspect/"

    PROJECT_CONTACT_NAME: str = "somespecialone"
    PROJECT_CONTACT_EMAIL: str = "tkachenkodmitriy@yahoo.com"

    PROJECT_LICENSE_NAME: str = "MIT"
    PROJECT_LICENSE_URL: AnyUrl = "https://github.com/somespecialone/clever-inspect/blob/master/LICENSE"

    # core
    DB_URL: str = "sqlite+aiosqlite:///" + str(ROOT_DIR / "data/items-cache.sqlite")

    CRED_FILE: FilePath = ROOT_DIR / "cred.json"

    # schemas dir url to resolve files urls
    SCHEMAS_DIR_URL: AnyUrl = "https://raw.githubusercontent.com/somespecialone/csgo-items-db/master/schemas/"

    UPDATE_INTERVAL: Callable[[Any], int] = ONCE_EVERY.FOUR_HOURS
    INSPECT_TIMEOUT: int = 15


settings = AppSettings()
