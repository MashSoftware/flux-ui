from flask import Blueprint

grade = Blueprint(
    "grade",
    __name__,
    template_folder="../templates/grade",
)

from app.grade import routes  # noqa: E402,F401
