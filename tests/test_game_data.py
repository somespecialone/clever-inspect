import pytest

from app.services import game_data
from app.models import Item

from .data import INSPECT_ITEMS


# just make sure there is no exceptions
@pytest.mark.parametrize("inspect", INSPECT_ITEMS)
def test_get_info(client, inspect):
    item = Item.from_steamio_model(inspect)
    info = game_data.get_item_info(item.to_dict())
    pass  # for breakpoint
