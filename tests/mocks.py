from unittest.mock import AsyncMock

import pytest
from steam_tradeoffer_manager.base import SteamBot, SteamBotPool
from pytest_mock import MockerFixture

from app.services.pool import InspectPool, InspectBot


__all__ = ("mock_bot", "mock_pool")


@pytest.fixture(scope="session", autouse=True)
def mock_bot(session_mocker: MockerFixture):
    session_mocker.patch.object(SteamBot, "on_ready", AsyncMock())
    session_mocker.patch.object(SteamBot, "is_ready", lambda _: True)
    session_mocker.patch.object(InspectBot, "request_free_license", AsyncMock())


async def startup(self: InspectPool):
    for bot in self:
        await bot.on_ready()


@pytest.fixture(scope="session", autouse=True)
def mock_pool(session_mocker: MockerFixture):
    session_mocker.patch.object(SteamBotPool, "startup", startup)
    session_mocker.patch.object(SteamBotPool, "shutdown", AsyncMock())
