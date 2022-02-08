import json
from typing import TypeAlias

from aiohttp import ClientSession

from .models import Item

_DEF_DICT: TypeAlias = "dict[str, str]"
_SCHEMA_ITEM: TypeAlias = "dict[str, str | _DEF_DICT]"


class GameData:
    __slots__ = (
        "schemas_dir_url",
        "_phases",
        "_wears",
        "_origins",
        "_qualities",
        "_types",
        "_paints",
        "_rarities",
        "_categories",
        "_tints",
        "_items",
        "_sticker_kits",
        "_cases",
    )

    _phases: _DEF_DICT
    _wears: list[dict[str, list[float] | str]]
    _origins: _DEF_DICT
    _qualities: _DEF_DICT
    _types: dict[str, _DEF_DICT]
    _paints: dict[str, dict[str, str | float]]
    _rarities: dict[str, _DEF_DICT]
    _categories: _DEF_DICT
    _tints: _DEF_DICT

    _items: dict[str, _DEF_DICT]
    _sticker_kits: dict[str, _DEF_DICT]
    _cases: dict[str, dict[str, str | list[str]]]

    _WEAPONS_RARITIES_CATEGORIES = {
        "knife",
        "pistol",
        "rifle",
        "smg",
        "sniper rifle",
        "shotgun",
        "machinegun",
        "gloves",
    }
    _WEAPON_KEY: str = "weapon"
    _NON_WEAPON_KEY: str = "nonweapon"
    _CHARACTER_KEY: str = "character"

    def __init__(self, schemas_dir_url: str):
        self.schemas_dir_url = schemas_dir_url

    async def load(self):
        await self._load()

    async def _load_parse_file(self, attr: str, session: ClientSession):
        resp = await session.get(self.schemas_dir_url + attr[1:] + ".json")
        setattr(self, attr, json.loads(await resp.text()))

    async def _load(self) -> None:
        async with ClientSession() as session:
            for attr in self.__slots__[1:]:
                await self._load_parse_file(attr, session)

    def _add_rarity(self, schema_item: _SCHEMA_ITEM):
        rarity_schema = self._rarities[schema_item["rarity"]]
        if schema_item["type"]["category"] in self._WEAPONS_RARITIES_CATEGORIES:
            rarity_key = self._WEAPON_KEY
        elif schema_item["type"]["category"] == "agent":
            rarity_key = self._CHARACTER_KEY
        else:
            rarity_key = self._NON_WEAPON_KEY

        rarity = {"color": rarity_schema["color"]}
        if rarity_name := rarity_schema.get(rarity_key):
            rarity["name"] = rarity_name

        schema_item["rarity"] = rarity

    def _add_type(self, schema_item: _SCHEMA_ITEM):
        item_type = {**self._types[schema_item["type"]]}
        item_type["category"] = self._categories[item_type["category"]]

        schema_item["type"] = item_type

    def _add_schema_item(self, item: Item):
        schema_item: _SCHEMA_ITEM = {}

        if item["paintindex"]:  # if paintable
            schema_item |= self._items[f"[{item['paintindex']}]{item['defindex']}"]
            schema_item["paint"] = self._paints[schema_item["paint"]]

            cases = []
            for case_id in schema_item.get("cases", []):
                cases.append(self._cases[case_id])

            if schema_item["paint"].get("phase"):
                schema_item["paint"]["phase"] = self._phases[schema_item["paint"]["phase"]]

        else:
            schema_item |= self._items[str(item["defindex"])]

        self._add_type(schema_item)
        self._add_rarity(schema_item)

        item["item"] = schema_item

    def _add_quality_name(self, item: Item):
        """Add and patch quality name"""
        item["quality_name"] = self._qualities[str(item["quality"])]

        # patch for items that are stattrak and ★ (★ Stattrak™ Karambit)
        if item["killeatervalue"] is not None and item["quality"] != 9:
            item["quality_name"] += " " + self._qualities["9"]

    def _add_wear_name(self, item: Item):
        if item["paintindex"]:  # if paintable and have wear
            for wear in self._wears:
                if wear["range"][0] <= item["paintwear"] < wear["range"][1]:
                    item["wear_name"] = wear["name"]
                    return

    def _add_origin_name(self, item: Item):
        item["origin_name"] = self._origins[str(item["origin"])]

    def _add_stickers(self, item: Item):
        for sticker in item["stickers"]:
            sticker["sticker_kit"] = self._sticker_kits[str(sticker["id"])]
            if tint_id := sticker.get("tint_id"):
                sticker["tint_name"] = self._tints[str(tint_id)]

    def get_item_info(self, inspected_item_data: dict) -> Item:
        item = Item(**inspected_item_data)

        self._add_schema_item(item)

        self._add_quality_name(item)
        self._add_wear_name(item)
        self._add_origin_name(item)

        self._add_stickers(item)

        return item
