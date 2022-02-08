import logging
import asyncio

from steam.ext.csgo import Client
from steam.ext.csgo.enums import Language
from steam.ext.csgo.backpack import BaseInspectedItem
from steam.protobufs import GCMsgProto, EMsg, MsgProto
from steam.protobufs.client_server import CMsgClientLicenseListLicense

from steam_tradeoffer_manager.base import SteamBot, SteamBotPool

_log = logging.getLogger(__name__)


# https://steamdb.info/app/730/subs/
_CSGO_PACKAGE_IDS = {
    17039,
    88535,
    54029,
    161243,
    261665,
    14,
    211096,
    133828,
    4,
    49,
    16236,
    16237,
    17878,
    18702,
    18703,
    18939,
    27267,
    29197,
    29198,
    36071,
    39221,
    39297,
    51835,
    51836,
    53711,
    59228,
    62690,
    88534,
    88541,
    88623,
    88624,
    61,
    392171,
    61986,
    329385,
    303386,
    63290,
    15740,
    298963,
    298962,
    298961,
    272766,
    199420,
    154735,
    277644,
    273865,
    266388,
    229740,
    226979,
    16222,
    16223,
    16018,
    16019,
    54030,
    63289,
    197847,
    4116,
    11470,
    11758,
    15990,
    17905,
    27618,
    27762,
    35043,
    54627,
    60765,
    62486,
    62606,
    62688,
    113904,
    124041,
    125313,
}

_CSGO_ID = 730


class InspectBot(SteamBot[int, "InspectPool"], Client):
    _licenses: dict[int, CMsgClientLicenseListLicense]

    async def on_ready(self) -> None:
        await super().on_ready()
        await asyncio.sleep(0.1)  # ensure licenses event was emitted

        for package_id in _CSGO_PACKAGE_IDS:
            if package_id in self.licenses:
                break
        else:
            # TODO: errors requesting free license
            _log.info(f"Request free CSGO license for {self}")
            await self.request_free_license([_CSGO_ID])  # request CSGO license

        self.pool.queue.put_nowait(self)

    @property
    def licenses(self) -> dict[int, CMsgClientLicenseListLicense]:
        return getattr(self, "_licenses", {})

    async def on_licenses(self, licenses: list[CMsgClientLicenseListLicense]):
        self._licenses = {}
        for steam_license in licenses:
            self.licenses[steam_license.package_id] = steam_license

    def timeout(self) -> asyncio.Task:
        async def _timeout():
            await asyncio.sleep(1)
            self.pool.queue.put_nowait(self)

        return asyncio.create_task(_timeout())

    def request_free_license(self, app_ids: list[int]):  # pragma: no cover
        return self.ws.send_proto_and_wait(MsgProto(EMsg.ClientRequestFreeLicense, appids=app_ids))

    async def inspect_item(self, s: int, a: int, d: int, m: int, timeout: int) -> BaseInspectedItem:  # pragma: no cover
        await self.ws.send_gc_message(
            GCMsgProto(
                Language.Client2GCEconPreviewDataBlockRequest,
                param_s=s,
                param_a=a,
                param_d=d,
                param_m=m,
            )
        )

        return await self.wait_for("inspect_item_info", timeout=timeout, check=lambda item: item.id == a)


class InspectPool(SteamBotPool[int, InspectBot]):
    INSPECT_TIMEOUT: int

    def __init__(self) -> None:
        super().__init__()
        self.queue: asyncio.Queue[InspectBot] = asyncio.Queue()

    async def startup(self) -> None:
        await super().startup()

        # waiting for first bot is ready and then return
        bot = await self.queue.get()
        self.queue.put_nowait(bot)

    async def inspect_item(self, s: int, a: int, d: int, m: int) -> BaseInspectedItem:
        bot = await self.queue.get()
        try:
            item = await bot.inspect_item(s, a, d, m, self.INSPECT_TIMEOUT)
        finally:
            bot.timeout()

        return item
