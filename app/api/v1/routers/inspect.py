import asyncio
from typing import Union

from fastapi import APIRouter, HTTPException, Depends

from app import schemas, models
from app.db import AsyncSession
from app.services import inspect_pool, game_data

from app.api.deps import get_session, ItemInspectParams

router = APIRouter(tags=["inspect"])


@router.get(
    "/",
    response_model=Union[schemas.Item, schemas.ItemRaw],
    response_model_exclude_defaults=True,
)
async def inspect_item(
    params: ItemInspectParams = Depends(ItemInspectParams),
    session: AsyncSession = Depends(get_session),
    raw: bool = False,
):

    if not (item_db := await session.get(models.Item, params.a)):  # check cash
        try:
            item_data = await inspect_pool.inspect_item(**params.dict())
        except asyncio.TimeoutError:
            # TODO error codes, more explicit exceptions
            raise HTTPException(500, {"error": "Steam servers not respond"})

        item_db: models.Item = models.Item.from_steamio_model(item_data)
        session.add(item_db)
        await session.commit()

    item_dict = item_db.to_dict()
    return game_data.get_item_info(item_dict) if not raw else item_dict
