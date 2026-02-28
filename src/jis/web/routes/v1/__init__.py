# web/routes/v1/__init__.py
# TODO: raw


from fastapi import APIRouter

from . import dashboard, vacancies, responses, analytics, system, account


v1_router = APIRouter()

v1_router.include_router(
    dashboard.router
)

v1_router.include_router(
    vacancies.router
)

v1_router.include_router(
    responses.router
)

v1_router.include_router(
    analytics.router
)

v1_router.include_router(
    system.router
)

v1_router.include_router(
    account.router
)


__all__ = [
    "v1_router"
]
