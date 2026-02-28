# static.py
# TODO: done


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .logger import get_logger


logger = get_logger(__name__)


def mount_static(app: FastAPI, static_dir: str = "src/jis/web/static") -> bool:
    static_path = Path(static_dir)

    if not static_path.exists():
        logger.warning(f"Static directory not found: {static_dir}")

        return False

    try:
        app.mount(
            "/static", StaticFiles(directory=str(static_path)), name="static"
        )

        logger.info("Static files mounted successfully!")

        return True
    except Exception as e:
        logger.error(f"Failed to mount static files: {e}")

        return False
