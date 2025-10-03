#!/usr/bin/env python3
"""
Script to help set up Supabase integration
"""

def get_supabase_info():
    print("=== Hướng dẫn lấy Supabase API Key ===")
    print()
    print("1. Truy cập: https://supabase.com/dashboard")
    print("2. Chọn project: iohaxfkciqvcoxsvzfyh")
    print("3. Vào Settings > API")
    print("4. Copy 'anon public' key")
    print()
    print("URL hiện tại: https://iohaxfkciqvcoxsvzfyh.supabase.co")
    print("Database URL: postgresql://postgres:25862586a@db.iohaxfkciqvcoxsvzfyh.supabase.co:5432/postgres")
    print()
    print("Sau khi có API key, cập nhật trong:")
    print("- extensions.py (dòng SUPABASE_KEY)")
    print("- Hoặc set environment variable: SUPABASE_KEY=your_key_here")

def test_current_setup():
    print("\n=== Kiểm tra setup hiện tại ===")
    
    # Test PostgreSQL
    try:
        import psycopg2
        conn = psycopg2.connect("postgresql://postgres:25862586a@db.iohaxfkciqvcoxsvzfyh.supabase.co:5432/postgres")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users;")
        user_count = cursor.fetchone()[0]
        print(f"✅ PostgreSQL: {user_count} users trong database")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ PostgreSQL: {e}")
    
    # Test Flask app
    try:
        from app import app
        from extensions import db
        with app.app_context():
            from models import User
            user_count = User.query.count()
            print(f"✅ Flask-SQLAlchemy: {user_count} users")
    except Exception as e:
        print(f"❌ Flask-SQLAlchemy: {e}")

if __name__ == "__main__":
    get_supabase_info()
    test_current_setup()