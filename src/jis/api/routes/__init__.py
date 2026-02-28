# api/routes/__init__.py
# TODO: raw


from fastapi import APIRouter


from .maintenance import maintenance_router
from .v1 import v1_router


api_router = APIRouter(prefix="/api")

api_router.include_router(
    maintenance_router,
    prefix="/maintenance"
)

api_router.include_router(
    v1_router,
    prefix="/v1"
)


__all__ = [
    "api_router"
]
