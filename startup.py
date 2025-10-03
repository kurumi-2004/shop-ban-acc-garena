#!/usr/bin/env python3
"""
Startup script for Render deployment
Automatically initializes database with data from init_db.py when Render starts
"""
import os
import sys
import time
from app import app, db
from models import User, GameAccount, PaymentSettings

def wait_for_database(max_retries=30, delay=2):
    """Wait for database to be ready"""
    for attempt in range(max_retries):
        try:
            with app.app_context():
                with db.engine.connect() as connection:
                    connection.execute(db.text('SELECT 1'))
                print(f"✅ Database ready after {attempt + 1} attempts")
                return True
        except Exception as e:
            print(f"⏳ Waiting for database... attempt {attempt + 1}/{max_retries}: {e}")
            time.sleep(delay)
    
    print("❌ Database not ready after maximum retries")
    return False

def auto_initialize_database():
    """Automatically initialize database on Render startup"""
    print("🚀 Starting Render deployment initialization...")
    
    # Wait for database to be ready
    if not wait_for_database():
        print("❌ Database connection failed, exiting...")
        sys.exit(1)
    
    try:
        with app.app_context():
            print(f"📊 Database URL: {app.config['SQLALCHEMY_DATABASE_URI'][:50]}...")
            
            # Create all tables
            db.create_all()
            print("✅ Database tables created/verified")
            
            # Check if database is empty
            user_count = User.query.count()
            account_count = GameAccount.query.count()
            payment_count = PaymentSettings.query.count()
            
            print(f"📈 Current database status:")
            print(f"   - Users: {user_count}")
            print(f"   - Accounts: {account_count}")
            print(f"   - Payment Settings: {payment_count}")
            
            # Auto-initialize if database is empty
            if user_count == 0 and account_count == 0:
                print("🔄 Database is empty, auto-initializing with sample data...")
                from init_db import init_database
                init_database()
                
                # Verify initialization
                new_user_count = User.query.count()
                new_account_count = GameAccount.query.count()
                new_payment_count = PaymentSettings.query.count()
                
                print("🎉 Auto-initialization completed!")
                print(f"   ✅ Created {new_user_count} users")
                print(f"   ✅ Created {new_account_count} game accounts")
                print(f"   ✅ Created {new_payment_count} payment settings")
                
            else:
                print("ℹ️ Database already has data, skipping initialization")
            
            print("✅ Render startup initialization completed successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Startup initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = auto_initialize_database()
    if not success:
        sys.exit(1)