import os
from app import create_app, db
from flask_migrate import Migrate
from dotenv import load_dotenv
import sys
import click

load_dotenv()
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
