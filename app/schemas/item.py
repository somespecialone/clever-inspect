from typing import Optional
from pydantic import BaseModel, HttpUrl, validator
from pydantic.color import Color

from .sticker import Sticker, StickerRaw
from .case import Case


class ItemRaw(BaseModel):
    id: int

    defindex: int

    rarity: int
    quality: int
    origin: int

    paintindex: Optional[int] = 0
    paintseed: Optional[int] = 0
    paintwear: Optional[float] = 0

    customname: Optional[str] = ""

    killeaterscoretype: Optional[int] = None
    killeatervalue: Optional[int] = None

    stickers: list[StickerRaw] = []

    # inventory: int
    # questid: int
    # dropreason: int
    # musicindex: int
    # ent_index: int

    # asset id can be bigint this size that json not support
    @validator("id")
    def int_to_str(cls, v: int):
        return str(v)

    @validator("paintwear")
    def round_float(cls, v: float):
        return round(v, 8)


class Type(BaseModel):
    category: str
    name: str


class Paint(BaseModel):
    name: str
    phase: Optional[str] = None

    wear_min: float
    wear_max: float


class Rarity(BaseModel):
    name: Optional[str] = None
    color: Color


class SchemaItem(BaseModel):
    image: HttpUrl

    type: Type
    paint: Optional[Paint] = None

    rarity: Rarity

    cases: list[Case] = []


class Item(ItemRaw):
    stickers: list[Sticker] = []

    item: SchemaItem

    quality_name: str
    wear_name: Optional[str] = None
    origin_name: str

    # @root_validator
    # def exclude_empty_fields(cls, data: dict[str, int | str | float | list]):
    #     return {k: v for k, v in data.items() if v}
