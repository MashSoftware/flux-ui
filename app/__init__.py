import logging

from config import Config
from flask import Flask
from flask_assets import Bundle, Environment
from flask_compress import Compress
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address, default_limits=["2 per second", "60 per minute"])
compress = Compress()
talisman = Talisman()
assets = Environment()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    assets.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    compress.init_app(app)
    csp = {
        "default-src": "'self'",
        "style-src": ["https://cdn.jsdelivr.net", "'self'"],
        "script-src": ["https://cdn.jsdelivr.net", "'self'"],
        "font-src": "https://cdn.jsdelivr.net",
        "img-src": ["data:", "'self'"],
    }
    talisman.init_app(app, content_security_policy=csp)

    js = Bundle("src/js/*.js", filters="jsmin", output="dist/js/custom-%(version)s.js")
    css = Bundle("src/css/*.css", filters="cssmin", output="dist/css/custom-%(version)s.css")
    if "js" not in assets:
        assets.register("js", js)
    if "css" not in assets:
        assets.register("css", css)

    # Register blueprints
    from app.grade import grade
    from app.main import main
    from app.organisation import organisation
    from app.practice import practice
    from app.programme import programme
    from app.project import project
    from app.role import role
    from app.person import person

    app.register_blueprint(main, url_prefix="/")
    app.register_blueprint(organisation, url_prefix="/organisations")
    app.register_blueprint(programme, url_prefix="/organisations")
    app.register_blueprint(project, url_prefix="/organisations")
    app.register_blueprint(grade, url_prefix="/organisations")
    app.register_blueprint(practice, url_prefix="/organisations")
    app.register_blueprint(role, url_prefix="/organisations")
    app.register_blueprint(person, url_prefix="/organisations")

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Startup")

    return app
