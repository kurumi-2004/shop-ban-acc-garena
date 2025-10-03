from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from cryptography.fernet import Fernet
from supabase import create_client, Client
import os

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

encryption_key = os.environ.get('ENCRYPTION_KEY', Fernet.generate_key())
cipher_suite = Fernet(encryption_key)

# Supabase configuration
SUPABASE_URL = "https://yxivfpnmtmkbaosmkkdo.supabase.co"
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl4aXZmcG5tdG1rYmFvc21ra2RvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk0MzU4NjMsImV4cCI6MjA3NTAxMTg2M30.IdS3OBvJpzPd03QWFJ7sB6-pVQrglvmF90SC06m4SQo')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
