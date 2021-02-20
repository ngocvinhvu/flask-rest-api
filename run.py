import os
from app import create_app, db
from flask_migrate import Migrate
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(basedir, '.env')
load_dotenv(dotenv_path)
app = create_app(os.getenv('FLASK_ENV') or 'default')
migrate = Migrate(app, db)
