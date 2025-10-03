from extensions import supabase, db
from app import app
import psycopg2
import os

def test_supabase_connection():
    """
    Kiểm tra kết nối với Supabase API
    """
    try:
        # Test với bảng users nếu có, hoặc tạo bảng test
        response = supabase.table('users').select('*').limit(1).execute()
        print("✅ Kết nối Supabase API thành công!")
        print(f"Dữ liệu: {response}")
        return True
    except Exception as e:
        print(f"❌ Lỗi kết nối Supabase API: {e}")
        return False

def test_postgresql_connection():
    """
    Kiểm tra kết nối PostgreSQL trực tiếp
    """
    try:
        conn_string = "postgresql://postgres:25862586a@db.iohaxfkciqvcoxsvzfyh.supabase.co:5432/postgres"
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print("✅ Kết nối PostgreSQL thành công!")
        print(f"PostgreSQL version: {version[0]}")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Lỗi kết nối PostgreSQL: {e}")
        return False

def test_flask_db_connection():
    """
    Kiểm tra kết nối database qua Flask-SQLAlchemy
    """
    try:
        with app.app_context():
            # Test connection using SQLAlchemy 2.0 syntax
            with db.engine.connect() as connection:
                result = connection.execute(db.text('SELECT 1'))
                print("✅ Kết nối Flask-SQLAlchemy thành công!")
                return True
    except Exception as e:
        print(f"❌ Lỗi kết nối Flask-SQLAlchemy: {e}")
        return False

if __name__ == "__main__":
    print("=== Kiểm tra kết nối Supabase ===")
    test_supabase_connection()
    print("\n=== Kiểm tra kết nối PostgreSQL ===")
    test_postgresql_connection()
    print("\n=== Kiểm tra kết nối Flask-SQLAlchemy ===")
    test_flask_db_connection()