#!/usr/bin/env python3
"""
Deployment script for production environment
"""
import os
import sys
from app import app, db
from models import User

def check_database():
    """Check if database is properly initialized"""
    try:
        with app.app_context():
            print(f"Database URL: {app.config['SQLALCHEMY_DATABASE_URI'][:50]}...")
            
            # Create tables if they don't exist
            db.create_all()
            print("✅ Database tables created/verified")
            
            # Try to query users table
            user_count = User.query.count()
            print(f"✅ Database connected. Found {user_count} users.")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def initialize_if_needed():
    """Initialize database if it's empty"""
    try:
        with app.app_context():
            # Check if tables exist and have data
            user_count = User.query.count()
            if user_count == 0:
                print("🔄 Database is empty, running initialization...")
                from init_db import init_database
                init_database()
                print("✅ Database initialized successfully!")
            else:
                print(f"✅ Database already has {user_count} users, skipping initialization.")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        sys.exit(1)

def run_startup_script():
    """Run startup script for automatic initialization"""
    try:
        from startup import auto_initialize_database
        return auto_initialize_database()
    except Exception as e:
        print(f"❌ Startup script failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Production Deployment Check ===")
    
    # Check environment variables
    required_vars = ['DATABASE_URL', 'SECRET_KEY']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        sys.exit(1)
    
    print("✅ Environment variables OK")
    
    # Run startup script for automatic initialization
    print("🚀 Running startup script...")
    if not run_startup_script():
        print("⚠️ Startup script failed, trying manual initialization...")
        if not check_database():
            print("🔄 Attempting to initialize database...")
            initialize_if_needed()
    
    print("✅ Deployment check completed successfully!")