# main.py
# TODO: done


from .core import setup_logging, mount_static
from .api import create_app, configure_routes


setup_logging()

app = create_app()

mount_static(app)

configure_routes(app)


# if __name__ == "__main__":
#     uvicorn.run(
#         "src.jis.main:app",
#         host=config.HOST,
#         port=config.PORT,
#         reload=config.RELOAD,
#         log_level=config.LOG_LEVEL.lower(),
#     )
