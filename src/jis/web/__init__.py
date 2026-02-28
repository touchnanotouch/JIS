# web/__init__.py
# TODO: done


from fastapi.templating import Jinja2Templates

from ..core import config


jinja_templates = Jinja2Templates(directory="src/jis/web/templates")
jinja_templates.env.globals["config"] = config


__all__ = [
    "jinja_templates"
]
