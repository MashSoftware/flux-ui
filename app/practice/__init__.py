from flask import Blueprint

practice = Blueprint(
    "practice",
    __name__,
    template_folder="../templates/practice/",
)

from app.practice import routes  # noqa: E402,F401
