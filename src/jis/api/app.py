from fastapi import FastAPI

from .routers import vacancies


def create_app() -> FastAPI:
    app = FastAPI(
        title="JIS API",
        description="JIS - Job Search Automation",
        version="0.1.0",
    )

    app.include_router(vacancies.router, prefix="/api/v1", tags=["vacancies"])

    @app.get("/")
    async def root():
        return {"message": "JIS API is running"}

    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": "JIS"}

    return app
