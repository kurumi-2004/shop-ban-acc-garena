#!/usr/bin/env python3
"""
Script to reset and initialize database with sample data
"""
from app import app, db
from models import User, GameAccount, Order, CartItem, AuditLog, Wishlist, PaymentSettings

def reset_database():
    """Reset database and add sample data"""
    with app.app_context():
        print("🔄 Resetting database...")
        
        # Drop all tables
        db.drop_all()
        print("✅ All tables dropped")
        
        # Create all tables
        db.create_all()
        print("✅ All tables created")
        
        # Initialize with sample data
        from init_db import init_database
        init_database()
        
        print("🎉 Database reset and initialized successfully!")

if __name__ == "__main__":
    reset_database()