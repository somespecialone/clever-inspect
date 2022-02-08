import os
import asyncio
import platform
import pathlib
import json

import pytest
from fastapi.testclient import TestClient

CRED_PATH = pathlib.Path("./cred.example.json").resolve()
os.environ["CRED_FILE"] = str(CRED_PATH)

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
def temp_cred_file():
    with CRED_PATH.open("r") as co:
        return json.load(co)


@pytest.fixture(scope="session", autouse=True)
def temp_db():
    config.settings.DB_URL = "sqlite+aiosqlite://"  # in memory


@pytest.fixture(scope="session")
def client():
    with TestClient(main.app) as test_client:
        yield test_client
