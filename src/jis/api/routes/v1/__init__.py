# api/routes/v1/__init__.py
# TODO: raw


from fastapi import APIRouter

from . import account


v1_router = APIRouter()

v1_router.include_router(
    account.router,
    prefix="/account"
)


__all__ = [
    "v1_router"
]
