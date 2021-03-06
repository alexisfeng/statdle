# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from flask_talisman import Talisman
from werkzeug.utils import secure_filename

# stdlib
from datetime import datetime
import os


db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()

from .users.routes import users
from .wordles.routes import wordles


def page_not_found(e):
    return render_template("404.html"), 404


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_pyfile("config.py", silent=False)
    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # talisman
    csp = {
        'default-src': [
            '\'self\''
        ],
        'img-src': '\'self\' data:',
        'style-src': [
            '\'self\'',
            'stackpath.bootstrapcdn.com'
        ],
        'script-src': [
            'stackpath.bootstrapcdn.com',
            'code.jquery.com',
            'cdn.jsdelivr.net'
        ]
    }
    Talisman(app, content_security_policy=csp)

    app.register_blueprint(users)
    app.register_blueprint(wordles)
    
    app.register_error_handler(404, page_not_found)

    login_manager.login_view = "users.login"

    app.config["MONGODB_HOST"] = os.getenv("MONGODB_HOST")

    return app
