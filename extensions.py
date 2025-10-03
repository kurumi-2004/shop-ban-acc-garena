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
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://iohaxfkciqvcoxsvzfyh.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlvaGF4ZmtjaXF2Y294c3Z6ZnloIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk1MDA1NDMsImV4cCI6MjA3NTA3NjU0M30.6KNWs3j2dnIW4ZlOJwO6gFOKK_gYxsQSyuuv0wj5_lo')

# Initialize Supabase client
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Warning: Could not initialize Supabase client: {e}")
    supabase = None
