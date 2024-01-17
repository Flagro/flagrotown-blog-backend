import os

from flask import Flask
from flask import request, abort
from flask_session import Session
from flask_cors import CORS
from .db import initialize_db
from .auth import initialize_auth
from .views.auth import auth_bp


def check_allowed_hosts(app):
    @app.before_request
    def before_request():
        host = request.headers.get('Host')
        if host not in app.config['ALLOWED_HOSTS']:
            abort(403)  # Forbidden access


def create_app(test_config=None):
    """Factory to create the Flask application
    :return: A `Flask` application instance
    """
    app = Flask(__name__)

    if os.environ.get('ENVIRONMENT') == 'development':
        allowed_hosts = ['localhost', '127.0.0.1', '0.0.0.0']
    else:
        allowed_hosts = ['blog.flagrotown.com']

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        ALLOWED_HOSTS=allowed_hosts,
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
    check_allowed_hosts(app)
    Session(app)
    CORS(app, supports_credentials=True)

    with app.app_context():
        db.create_all()

    return app


def _register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix="/auth")
