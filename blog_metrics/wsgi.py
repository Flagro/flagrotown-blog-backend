from app import create_app
from flask.cli import load_dotenv

load_dotenv(".env")
app = create_app()
