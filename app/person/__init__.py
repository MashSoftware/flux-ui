from flask import Blueprint

person = Blueprint(
    "person",
    __name__,
    template_folder="../templates/person/",
)

from app.person import routes  # noqa: E402,F401
