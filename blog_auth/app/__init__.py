import os

from flask import Flask
from flask_session import Session
from flask_cors import CORS
from .db import initialize_db
from .auth import initialize_auth
from .views.auth import auth_bp


def create_app(test_config=None):
    """Factory to create the Flask application
    :return: A `Flask` application instance
    """
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI="{}://{}:{}@{}:{}/{}".format(
            os.environ.get('DB_ENGINE'),
            os.environ.get('DB_USER'),
            os.environ.get('DB_PASSWORD'),
            os.environ.get('DB_HOST'),
            os.environ.get('DB_PORT'),
            os.environ.get('DB_NAME')
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_TYPE='sqlalchemy'
    )
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
