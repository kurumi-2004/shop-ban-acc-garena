from extensions import supabase

def test_connection():
    """
    Kiểm tra kết nối với Supabase
    """
    try:
        # Thử lấy dữ liệu từ bảng (thay thế 'test' bằng tên bảng thực tế nếu có)
        response = supabase.table('test').select('*').limit(1).execute()
        print("Kết nối Supabase thành công!")
        print(f"Dữ liệu: {response}")
        return True
    except Exception as e:
        print(f"Lỗi kết nối Supabase: {e}")
        return False

if __name__ == "__main__":
    test_connection()