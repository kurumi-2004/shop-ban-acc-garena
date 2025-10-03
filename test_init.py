#!/usr/bin/env python3
"""
Test initialization locally
"""
import os
from app import app, db
from models import User, GameAccount, PaymentSettings

def test_init():
    """Test database initialization"""
    print("=== Testing Database Initialization ===")
    
    with app.app_context():
        print(f"Database URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        # Check current status
        try:
            user_count = User.query.count()
            account_count = GameAccount.query.count()
            payment_count = PaymentSettings.query.count()
            
            print(f"Current status:")
            print(f"  Users: {user_count}")
            print(f"  Accounts: {account_count}")
            print(f"  Payment Settings: {payment_count}")
            
            if user_count == 0 and account_count == 0:
                print("🔄 Running initialization...")
                from init_db import init_database
                init_database()
                
                # Check after init
                new_user_count = User.query.count()
                new_account_count = GameAccount.query.count()
                new_payment_count = PaymentSettings.query.count()
                
                print(f"After initialization:")
                print(f"  Users: {new_user_count}")
                print(f"  Accounts: {new_account_count}")
                print(f"  Payment Settings: {new_payment_count}")
                
                print("✅ Initialization completed!")
            else:
                print("ℹ️ Database already has data")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_init()