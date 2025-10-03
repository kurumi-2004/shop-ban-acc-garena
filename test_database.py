#!/usr/bin/env python3
"""
Simple database connection test for Render PostgreSQL
"""
import os
from app import app, db
from models import User

def test_database_connection():
    """Test database connection"""
    try:
        with app.app_context():
            # Test basic connection using SQLAlchemy 2.0 syntax
            with db.engine.connect() as connection:
                connection.execute(db.text('SELECT 1'))
            print("✅ Database connection successful!")
            
            # Test table creation
            db.create_all()
            print("✅ Tables created/verified!")
            
            # Test user count
            user_count = User.query.count()
            print(f"✅ Found {user_count} users in database")
            
            return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing Render PostgreSQL Connection ===")
    
    database_url = os.environ.get('DATABASE_URL', 'Not set')
    print(f"Database URL: {database_url[:50]}..." if len(database_url) > 50 else database_url)
    
    if test_database_connection():
        print("✅ All database tests passed!")
    else:
        print("❌ Database tests failed!")