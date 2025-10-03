# Hướng dẫn triển khai trên Render

## Bước 1: Tạo tài khoản Render
1. Truy cập https://render.com
2. Đăng ký/Đăng nhập bằng GitHub account

## Bước 2: Kết nối GitHub Repository
1. Vào Dashboard của Render
2. Click "New +" → "Web Service"
3. Chọn "Connect a repository"
4. Tìm và chọn repository: `kurumi-2004/shop-ban-acc-garena`

## Bước 3: Cấu hình Web Service
Điền các thông tin sau:

**Name**: `shop-ban-acc-garena` (hoặc tên bạn muốn)

**Environment**: `Python 3`

**Build Command**: 
```
pip install -r requirements.txt
```

**Start Command**:
```
gunicorn app:app
```

**Instance Type**: `Free` (hoặc chọn plan phù hợp)

## Bước 4: Thêm Environment Variables
Click "Advanced" và thêm các biến môi trường:

1. **SECRET_KEY**: 
   - Click "Generate" để tạo key tự động
   - Hoặc nhập: `your-secret-key-here-change-this`

2. **DATABASE_URL**: 
   - Nếu dùng PostgreSQL của Render: Tạo database trước (xem bước 5)
   - Hoặc để trống để dùng SQLite (không khuyến khích cho production)

3. **FLASK_ENV**: `production`

4. **ENCRYPTION_KEY** (nếu cần):
   - Tạo key bằng Python:
   ```python
   from cryptography.fernet import Fernet
   print(Fernet.generate_key().decode())
   ```

## Bước 5: Tạo PostgreSQL Database (Khuyến nghị)
1. Trong Render Dashboard, click "New +" → "PostgreSQL"
2. Điền thông tin:
   - **Name**: `shop-db`
   - **Database**: `shop_acc_garena`
   - **User**: `shop_user`
   - **Region**: Chọn gần bạn nhất
   - **Instance Type**: `Free`
3. Click "Create Database"
4. Sau khi tạo xong, copy "Internal Database URL"
5. Quay lại Web Service, thêm biến `DATABASE_URL` với giá trị vừa copy

## Bước 6: Deploy
1. Click "Create Web Service"
2. Render sẽ tự động build và deploy
3. Đợi khoảng 5-10 phút
4. Khi deploy xong, bạn sẽ nhận được URL: `https://shop-ban-acc-garena.onrender.com`

## Bước 7: Khởi tạo Database
Sau khi deploy thành công, cần chạy migration:

1. Vào Web Service dashboard
2. Click tab "Shell"
3. Chạy lệnh:
```bash
flask db upgrade
python init_db.py
```

## Lưu ý quan trọng:
- Free tier của Render sẽ sleep sau 15 phút không hoạt động
- Lần đầu truy cập sau khi sleep sẽ mất ~30 giây để wake up
- Nếu muốn tránh sleep, cần upgrade lên paid plan
- Database free có giới hạn 1GB storage

## Cập nhật code:
Mỗi khi push code mới lên GitHub branch `main`, Render sẽ tự động deploy lại.

## Troubleshooting:
- Nếu deploy fail, check logs trong tab "Logs"
- Đảm bảo `requirements.txt` có đầy đủ dependencies
- Kiểm tra `Procfile` và `render.yaml` đã đúng format

## URL sau khi deploy:
https://shop-ban-acc-garena.onrender.com (hoặc tên bạn đặt)
