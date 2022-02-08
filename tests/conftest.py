import os
import asyncio
import platform
import pathlib
import json

import pytest
from fastapi.testclient import TestClient

# set env vars before settings instance will be constructed
CRED_PATH = pathlib.Path("./cred.example.json").resolve()
os.environ["CRED_FILE"] = str(CRED_PATH)
os.environ["DB_URL"] = "sqlite+aiosqlite://"  # in memory

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


@pytest.fixture(scope="session")
def client():
    from app import main

    with TestClient(main.app) as test_client:
        yield test_client
