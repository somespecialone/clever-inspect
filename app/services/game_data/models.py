from typing import TypedDict


class Sticker(TypedDict, total=False):
    slot: int
    id: int
    wear: float
    scale: float
    rotation: float
    tint_id: int

    sticker_kit: dict
    tint_name: str


class Item(TypedDict, total=False):
    id: int
    defindex: int
    paintindex: int
    paintseed: int
    paintwear: float
    rarity: int
    quality: int
    killeaterscoretype: int
    killeatervalue: int
    customname: str
    inventory: int
    origin: int
    questid: int
    dropreason: int
    musicindex: int
    ent_index: int

    stickers: list[Sticker]

    item: dict
    quality_name: str
    wear_name: str
    origin_name: str
