from unittest.mock import AsyncMock

import pytest
from pytest_mock import MockerFixture

from app.services.pool import InspectBot

from .data import INSPECT_ITEMS, INVALID_PARAMS, PARAMS


def test_health(client, temp_cred_file):
    resp = client.get("v1/health").json()

    assert resp["online"] == len(temp_cred_file)
    assert resp["total"] == len(temp_cred_file)
    assert resp["concurrency"] == len(temp_cred_file)


@pytest.mark.parametrize("params", INVALID_PARAMS)
def test_inspect_params_missing(client, params):
    resp = client.get("v1/", params=params)

    assert resp.status_code == 400


@pytest.mark.parametrize("params", PARAMS)
def test_inspect(mocker: MockerFixture, client, params):
    mocker.patch.object(InspectBot, "inspect_item", AsyncMock(return_value=INSPECT_ITEMS[0]))
    resp = client.get("v1/", params=params).json()

    assert int(resp["id"]) == INSPECT_ITEMS[0].id


@pytest.mark.parametrize("params", PARAMS)
def test_inspect_raw(mocker: MockerFixture, client, params):
    mocker.patch.object(InspectBot, "inspect_item", AsyncMock(return_value=INSPECT_ITEMS[0]))
    resp = client.get("v1/", params={**params, "raw": True}).json()

    assert int(resp["id"]) == INSPECT_ITEMS[0].id
