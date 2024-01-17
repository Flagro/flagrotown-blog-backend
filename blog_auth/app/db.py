from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = None

def initialize_db(app):
    db.init_app(app)

    global migrate
    migrate = Migrate(app, db)
