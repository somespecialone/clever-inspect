from typing import Optional, Literal

from pydantic import BaseModel, HttpUrl, validator


class StickerBase(BaseModel):
    slot: Literal[0, 1, 2, 3, 4]
    wear: Optional[float] = 0

    @validator("wear")
    def round_float(cls, v: float):
        return round(v, 2)


class StickerRaw(StickerBase):
    id: int

    tint_id: Optional[int] = 0

    # scale: float
    # rotation: float


class StickerKit(BaseModel):
    name: str
    image: HttpUrl


class Sticker(StickerBase):
    sticker_kit: StickerKit
    tint_name: Optional[str] = None
