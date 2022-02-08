from fastapi import APIRouter

from . import v1

router = APIRouter()
endpoints = (v1,)


for endpoint in endpoints:
    router.include_router(endpoint.router)
