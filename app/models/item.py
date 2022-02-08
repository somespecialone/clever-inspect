from typing import Any
from sqlalchemy import Column, BigInteger, JSON

from ..db import BaseModel

from steam.ext.csgo.backpack import BaseInspectedItem


class Item(BaseModel):
    __tablename__ = "items"

    id = Column(BigInteger, primary_key=True)

    data: dict[str, Any] = Column(JSON)

    def to_dict(self) -> dict:
        return {"id": self.id, **self.data}

    @classmethod
    def from_steamio_model(cls, model: BaseInspectedItem) -> "Item":
        return cls(
            id=model.id,
            data={
                "defindex": model.def_index,
                "paintindex": model.paint.index,
                "rarity": model.rarity,
                "quality": model.quality,
                "paintwear": model.paint.wear,  # decoded
                "paintseed": model.paint.seed,
                "killeaterscoretype": model.kill_eater_score_type,
                "killeatervalue": model.kill_eater_value,
                "customname": model.custom_name,
                "stickers": [
                    {
                        "slot": sticker.slot,
                        "id": sticker.id,
                        "wear": sticker.wear,
                        "scale": sticker.scale,
                        "rotation": sticker.rotation,
                        "tint_id": sticker.tint_id,
                    }
                    for sticker in model.stickers
                ],
                "inventory": model.inventory,
                "origin": model.origin,
                "questid": model.quest_id,
                "dropreason": model.drop_reason,
                "musicindex": model.music_index,
                "entindex": model.ent_index,
            },
        )
