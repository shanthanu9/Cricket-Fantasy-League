from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# The flask app
app = Flask(__name__)
# Configure app
app.config.from_object(Config)
# Set database and migrations
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Login handler
login = LoginManager(app)
login.login_view = 'login' # Helpful for forcing anonymous users to login

from app import routes, models