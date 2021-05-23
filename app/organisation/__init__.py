from flask import Blueprint

organisation = Blueprint(
    "organisation",
    __name__,
    template_folder="../templates/organisation/",
)

from app.organisation import routes  # noqa: E402,F401
