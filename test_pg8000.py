#!/usr/bin/env python3
"""
Test pg8000 PostgreSQL driver compatibility
"""
import os

def test_pg8000_connection():
    """Test pg8000 driver connection"""
    try:
        import pg8000
        print("✅ pg8000 driver imported successfully")
        
        # Test connection
        conn = pg8000.connect(
            host="db.iohaxfkciqvcoxsvzfyh.supabase.co",
            port=5432,
            user="postgres",
            password="25862586a",
            database="postgres"
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ pg8000 connection successful!")
        print(f"PostgreSQL version: {version[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ pg8000 connection failed: {e}")
        return False

def test_sqlalchemy_with_pg8000():
    """Test SQLAlchemy with pg8000 driver"""
    try:
        from sqlalchemy import create_engine, text
        
        # Test with pg8000 driver
        engine = create_engine('postgresql+pg8000://postgres:25862586a@db.iohaxfkciqvcoxsvzfyh.supabase.co:5432/postgres')
        
        with engine.connect() as connection:
            result = connection.execute(text('SELECT 1'))
            print("✅ SQLAlchemy with pg8000 works!")
            return True
            
    except Exception as e:
        print(f"❌ SQLAlchemy with pg8000 failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing pg8000 PostgreSQL Driver ===")
    test_pg8000_connection()
    print("\n=== Testing SQLAlchemy with pg8000 ===")
    test_sqlalchemy_with_pg8000()