from app.core.config import settings
from app.core.logging import setup_logging


async def logging_startup():
    setup_logging(debug=settings.DEBUG)
