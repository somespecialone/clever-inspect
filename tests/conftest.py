import asyncio
import platform
import json

import pytest
from fastapi.testclient import TestClient

from app import main
from app.core import config

from .mocks import *


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    """Prevent warning on Windows"""
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.get_event_loop_policy().new_event_loop()


@pytest.fixture(scope="session", autouse=True)
def temp_cred_file(tmp_path_factory):
    c = tmp_path_factory.mktemp("temp") / "cred.json"
    c.touch()
    with (config.settings.ROOT_DIR / "cred.example.json").open("r") as e:
        example = json.load(e)
    with c.open("w") as co:
        json.dump(example, co)

    config.settings.CRED_FILE = c

    with c.open("r") as co:
        return json.load(co)


@pytest.fixture(scope="session", autouse=True)
def temp_db():
    config.settings.DB_URL = "sqlite+aiosqlite://"  # in memory


@pytest.fixture(scope="session")
def client():
    with TestClient(main.app) as test_client:
        yield test_client
