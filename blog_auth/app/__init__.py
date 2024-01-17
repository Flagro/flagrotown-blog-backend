import os

from flask import Flask
from flask_session import Session
from flask.cli import load_dotenv
from flask_cors import CORS
from .db import initialize_db
from .auth import initialize_auth
from .views.auth import auth_bp


def create_app(test_config=None):
    """Factory to create the Flask application
    :return: A `Flask` application instance
    """
    app = Flask(__name__)
    load_dotenv(".env")
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config["EXTERNAL_API_URL"] = os.environ.get("EXTERNAL_API_URL")
    if test_config:
        app.config.update(test_config)
    _register_blueprints(app)
    initialize_db(app)
    initialize_auth(app)
    Session(app)
    CORS(app, supports_credentials=True)

    with app.app_context():
        db.create_all()

    return app


def _register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix="/auth")
