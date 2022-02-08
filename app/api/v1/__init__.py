from fastapi import APIRouter

from .routers import health, inspect

router = APIRouter(prefix="/v1")
endpoints = (health, inspect)


for endpoint in endpoints:
    router.include_router(endpoint.router)
