# api/routes/maintenance.py
# TODO: done


import platform

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from datetime import datetime

from ...core import config, db_manager, redis_manager, celery_manager


maintenance_router = APIRouter(tags=["Maintenance"])


@maintenance_router.get("/health")
async def get_health() -> JSONResponse:
    db_status: bool = db_manager.health_check()
    redis_status: bool = await redis_manager.health_check()
    celery_status: bool = (
        celery_manager.health_check()
        if hasattr(celery_manager, "health_check")
        else False
    )

    status: bool = all([db_status, redis_status, celery_status])

    return JSONResponse(
        content={
            "status": "healthy" if all([db_status, redis_status]) else "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "components": {
                "database": "healthy" if db_status else "unhealthy",
                "redis": "healthy" if redis_status else "unhealthy",
                "celery": "healthy" if celery_status else "not_configured",
            },
            "version": config.GIT_TAG,
            "commit": config.GIT_COMMIT_HASH,
            "environment": config.ENVIRONMENT,
        },
        status_code=200 if status else 503
    )

@maintenance_router.get("/health/database")
async def get_health_database() -> JSONResponse:
    status: bool = db_manager.health_check()

    return JSONResponse(
        content={"status": "healthy" if status else "unhealthy"},
        status_code=200 if status else 503
    )

@maintenance_router.get("/health/redis")
async def get_health_redis() -> JSONResponse:
    status = await redis_manager.health_check()

    return JSONResponse(
        content={"status": "healthy" if status else "unhealthy"},
        status_code=200 if status else 503,
    )

@maintenance_router.get("/health/celery")
async def get_health_celery() -> JSONResponse:
    if hasattr(celery_manager, "health_check"):
        status = celery_manager.health_check()

        return JSONResponse(
            content={"status": "healthy" if status else "unhealthy"},
            status_code=200 if status else 503,
        )

    return JSONResponse(content={"status": "not_configured"}, status_code=200)

@maintenance_router.get("/info")
async def get_info():
    return {
        "version": config.GIT_TAG,
        "commit_hash": config.GIT_COMMIT_HASH,
        "commit_date": config.GIT_COMMIT_DATE,
        "environment": config.ENVIRONMENT,
        "debug": config.DEBUG,
        "python_version": platform.python_version()
    }
