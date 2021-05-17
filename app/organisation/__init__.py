from flask import Blueprint

bp = Blueprint("organisation", __name__, url_prefix="/organisation", template_folder="templates")

from app.organisation import routes  # noqa: E402,F401
