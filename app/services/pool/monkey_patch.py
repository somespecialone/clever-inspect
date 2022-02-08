"""Patch to properly decode item wear and send item inspect info"""

import asyncio
import logging

from steam import state


log = logging.getLogger(__name__)


# avoid key errors for bot's without api key while we don't need trade offers management
async def poll_trades_patched(*args, **kwargs):
    await asyncio.sleep(0)


state.ConnectionState.poll_trades = poll_trades_patched


from steam.models import register
from steam.protobufs.client_server import CMsgClientLicenseList
from steam.protobufs.emsg import EMsg


#  emit licenses
@register(EMsg.ClientLicenseList)
def handle_licenses(self: state.ConnectionState, msg: state.MsgProto[CMsgClientLicenseList]):
    self.dispatch("licenses", msg.body.licenses)


state.ConnectionState.handle_licenses = handle_licenses

log.debug("Monkey patch imported")
