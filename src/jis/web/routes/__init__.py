# web/routes/__init__.py
# TODO: done


from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from .v1 import v1_router


web_router = APIRouter()

web_router.include_router(
    v1_router
)


@web_router.get("/", include_in_schema=False)
async def get_root():
    return RedirectResponse(url="/dashboard")


__all__ = [
    "web_router"
]
