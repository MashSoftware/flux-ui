from flask import Blueprint

project = Blueprint(
    "project",
    __name__,
    template_folder="../templates/project",
)

from app.project import routes  # noqa: E402,F401
