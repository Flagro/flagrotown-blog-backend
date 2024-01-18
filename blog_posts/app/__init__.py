import os

from flask import Flask
from flask import request, abort
from flask_cors import CORS
from .db import initialize_db
from .auth import initialize_auth
from .object_storage import initialize_object_storage
from .views.posts import posts_bp
from .views.blog_repo import blog_repo_bp


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
        BLOG_GITHUB_WEBHOOK_SECRET=os.environ.get('BLOG_GITHUB_WEBHOOK_SECRET'),
        BLOG_GITHUB_REPO_URL=os.environ.get('BLOG_GITHUB_REPO_URL'),
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
        SESSION_TYPE='sqlalchemy',
        AWS_REGION=os.environ.get('AWS_REGION'),
        AWS_ACCESS_KEY_ID=os.environ.get('AWS_ACCESS_KEY_ID'),
        AWS_SECRET_ACCESS_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        AWS_S3_ENDPOINT_URL=os.environ.get('AWS_S3_ENDPOINT_URL'),
        AWS_S3_BUCKET_NAME=os.environ.get('AWS_S3_BUCKET_NAME'),
    )
    if test_config:
        app.config.update(test_config)
    _register_blueprints(app)
    initialize_db(app)
    initialize_auth(app)
    initialize_object_storage(app)
    check_allowed_hosts(app)
    CORS(app, supports_credentials=True)

    return app


def _register_blueprints(app):
    app.register_blueprint(posts_bp, url_prefix="/posts")
    app.register_blueprint(blog_repo_bp, url_prefix="/posts")
