from flask import Blueprint

role = Blueprint(
    "role",
    __name__,
    template_folder="../templates/role/",
)

from app.role import routes  # noqa: E402,F401
