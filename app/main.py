from fastapi import FastAPI

from app.api import router as api_router
from app.core.config import settings
from app.hooks import game_data_startup, db_startup, db_shutdown, pool_startup, pool_shutdown, logging_startup

on_startup = (logging_startup, game_data_startup, db_startup, pool_startup)  # pool should start last
on_shutdown = (pool_shutdown, db_shutdown)  # and shutdown first

app = FastAPI(
    debug=settings.DEBUG,
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    # meta
    title=settings.PROJECT_TITLE,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    terms_of_service=settings.PROJECT_TERMS_OF_SERVICE,
    contact={
        "name": settings.PROJECT_CONTACT_NAME,
        "email": settings.PROJECT_CONTACT_EMAIL,
    },
    license_info={
        "name": settings.PROJECT_LICENSE_NAME,
        "url": settings.PROJECT_LICENSE_URL,
    },
)

app.include_router(api_router)
