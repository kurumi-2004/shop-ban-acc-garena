from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from cryptography.fernet import Fernet
import os

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

encryption_key = os.environ.get('ENCRYPTION_KEY', Fernet.generate_key())
cipher_suite = Fernet(encryption_key)
