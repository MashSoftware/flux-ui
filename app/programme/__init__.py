from flask import Blueprint

programme = Blueprint(
    "programme",
    __name__,
    template_folder="../templates/programme",
)

from app.programme import routes  # noqa: E402,F401
