import os
from app import app, db
from models import User, GameAccount, Order, CartItem, AuditLog
from extensions import cipher_suite

def init_database():
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        if User.query.first() is None:
            print("Adding sample data...")
            
            superadmin = User(
                email='superadmin@shopaccgarena.vn',
                username='superadmin',
                full_name='Super Admin',
                phone='0912345678',
                is_admin=True,
                role='superadmin'
            )
            superadmin.set_password('SuperAdmin@2024!Secure')
            db.session.add(superadmin)
            
            admin = User(
                email='admin@shopaccgarena.vn',
                username='admin',
                full_name='Quản trị viên',
                phone='0912345679',
                is_admin=True,
                role='admin'
            )
            admin.set_password('Admin@2024!Secure')
            db.session.add(admin)
            
            support = User(
                email='support@shopaccgarena.vn',
                username='support',
                full_name='Nhân viên hỗ trợ',
                phone='0912345680',
                is_admin=True,
                role='support'
            )
            support.set_password('Support@2024!Secure')
            db.session.add(support)
            
            user = User(
                email='user@example.com',
                username='testuser',
                full_name='Nguyễn Văn A',
                phone='0987654321',
                is_admin=False,
                role='user'
            )
            user.set_password('user123')
            db.session.add(user)
            
            accounts_data = [
                {
                    'title': 'Tài khoản Premium Elite',
                    'description': 'Tài khoản premium cao cấp với nhiều trang bị hiếm. Đã chơi lâu năm, có nhiều skin độc quyền.',
                    'category': 'Premium',
                    'rank': 'Elite',
                    'price': 500000,
                    'username': 'premiumuser01',
                    'password': 'Pass@2024'
                },
                {
                    'title': 'Tài khoản VIP Rank Cao',
                    'description': 'VIP với rank cao, nhiều thành tích. Phù hợp cho người muốn chơi ở cấp độ cao.',
                    'category': 'VIP',
                    'rank': 'Cao',
                    'price': 750000,
                    'username': 'vipuser01',
                    'password': 'VipPass123'
                },
                {
                    'title': 'Tài khoản Standard',
                    'description': 'Tài khoản tiêu chuẩn cho người mới bắt đầu. Có đầy đủ tính năng cơ bản.',
                    'category': 'Standard',
                    'rank': 'Trung bình',
                    'price': 200000,
                    'username': 'standard01',
                    'password': 'Std2024'
                },
                {
                    'title': 'Tài khoản Special Edition',
                    'description': 'Phiên bản đặc biệt với các vật phẩm giới hạn. Không có nhiều trên thị trường.',
                    'category': 'Special',
                    'rank': 'Elite',
                    'price': 1200000,
                    'username': 'special01',
                    'password': 'Special@123'
                },
                {
                    'title': 'Tài khoản Premium Starter',
                    'description': 'Premium cho người mới với nhiều ưu đãi khởi đầu. Dễ dàng phát triển.',
                    'category': 'Premium',
                    'rank': 'Thấp',
                    'price': 350000,
                    'username': 'premstarter01',
                    'password': 'Start@2024'
                },
                {
                    'title': 'Tài khoản VIP Pro',
                    'description': 'VIP Pro với đầy đủ tính năng cao cấp nhất. Trải nghiệm tốt nhất.',
                    'category': 'VIP',
                    'rank': 'Elite',
                    'price': 980000,
                    'username': 'vippro01',
                    'password': 'Pro@VIP2024'
                },
                {
                    'title': 'Tài khoản Standard Plus',
                    'description': 'Nâng cấp từ bản standard với thêm nhiều tính năng. Giá cả phải chăng.',
                    'category': 'Standard',
                    'rank': 'Trung bình',
                    'price': 280000,
                    'username': 'stdplus01',
                    'password': 'StdPlus123'
                },
                {
                    'title': 'Tài khoản Premium Master',
                    'description': 'Master level premium với tất cả unlock. Dành cho người chơi chuyên nghiệp.',
                    'category': 'Premium',
                    'rank': 'Elite',
                    'price': 1500000,
                    'username': 'master01',
                    'password': 'Master@Pro'
                }
            ]
            
            for acc_data in accounts_data:
                encrypted_username = cipher_suite.encrypt(acc_data['username'].encode()).decode()
                encrypted_password = cipher_suite.encrypt(acc_data['password'].encode()).decode()
                
                account = GameAccount(
                    title=acc_data['title'],
                    description=acc_data['description'],
                    category=acc_data['category'],
                    rank=acc_data['rank'],
                    price=acc_data['price'],
                    account_username=encrypted_username,
                    account_password=encrypted_password,
                    is_sold=False
                )
                db.session.add(account)
            
            db.session.commit()
            print("Sample data added successfully!")
            print("\n=== IMPORTANT: Admin Credentials (DO NOT SHARE) ===")
            print("\nSuper Admin: superadmin@shopaccgarena.vn / SuperAdmin@2024!Secure")
            print("Admin: admin@shopaccgarena.vn / Admin@2024!Secure")
            print("Support: support@shopaccgarena.vn / Support@2024!Secure")
            print("\n=== Public Demo Account ===")
            print("User Demo: user@example.com / user123")
            print("\nNOTE: Admin passwords are complex and should be changed in production!")
        else:
            print("Database already initialized!")

if __name__ == '__main__':
    init_database()
