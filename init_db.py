import os
from app import app, db
from models import User, GameAccount, Order, CartItem, AuditLog, PaymentSettings
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
            
            db.session.commit()
            print("User accounts added successfully!")
            
            # Add sample game accounts
            print("Adding sample game accounts...")
            
            sample_accounts = [
                {
                    'title': 'Liên Quân Mobile - Tướng Đầy Đủ',
                    'description': 'Tài khoản Liên Quân Mobile với đầy đủ tướng, skin hiếm. Rank Cao Thủ 5 sao.',
                    'category': 'Liên Quân Mobile',
                    'rank': 'Cao Thủ',
                    'price': 500000,
                    'username': 'lqm_account_01',
                    'password': 'password123'
                },
                {
                    'title': 'Free Fire - Tài Khoản VIP',
                    'description': 'Tài khoản Free Fire với nhiều skin súng, nhân vật hiếm. Rank Thách Đấu.',
                    'category': 'Free Fire',
                    'rank': 'Thách Đấu',
                    'price': 300000,
                    'username': 'ff_vip_account',
                    'password': 'ff123456'
                },
                {
                    'title': 'PUBG Mobile - Conqueror',
                    'description': 'Tài khoản PUBG Mobile rank Conqueror, có nhiều outfit và skin súng đẹp.',
                    'category': 'PUBG Mobile',
                    'rank': 'Conqueror',
                    'price': 800000,
                    'username': 'pubg_conqueror',
                    'password': 'pubg2024'
                },
                {
                    'title': 'Liên Quân Mobile - Skin Murad Rồng',
                    'description': 'Tài khoản có skin Murad Rồng cực hiếm, rank Thách Đấu 100 sao.',
                    'category': 'Liên Quân Mobile',
                    'rank': 'Thách Đấu',
                    'price': 1200000,
                    'username': 'murad_dragon',
                    'password': 'dragon123'
                },
                {
                    'title': 'Free Fire - Tài Khoản Streamer',
                    'description': 'Tài khoản Free Fire của streamer nổi tiếng, có badge đặc biệt.',
                    'category': 'Free Fire',
                    'rank': 'Grandmaster',
                    'price': 600000,
                    'username': 'ff_streamer',
                    'password': 'stream2024'
                },
                {
                    'title': 'Mobile Legends - Mythic Glory',
                    'description': 'Tài khoản Mobile Legends rank Mythic Glory với đầy đủ hero và skin.',
                    'category': 'Mobile Legends',
                    'rank': 'Mythic Glory',
                    'price': 700000,
                    'username': 'ml_mythic',
                    'password': 'mythic123'
                }
            ]
            
            for acc_data in sample_accounts:
                # Encrypt username and password
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
                    is_sold=False,
                    images=[]
                )
                db.session.add(account)
            
            db.session.commit()
            print(f"✅ Added {len(sample_accounts)} sample game accounts!")
            
            # Add default payment settings
            print("Adding default payment settings...")
            payment_settings = PaymentSettings(
                bank_id='970422',  # MB Bank
                bank_name='MB Bank',
                account_number='0123456789',
                account_name='SHOP BAN ACC GARENA',
                qr_template='compact',
                is_active=True
            )
            db.session.add(payment_settings)
            db.session.commit()
            print("✅ Default payment settings added!")
            
            print("\n=== IMPORTANT: Admin Credentials (DO NOT SHARE) ===")
            print("\nSuper Admin: superadmin@shopaccgarena.vn / SuperAdmin@2024!Secure")
            print("Admin: admin@shopaccgarena.vn / Admin@2024!Secure")
            print("Support: support@shopaccgarena.vn / Support@2024!Secure")
            print("\n=== Public Demo Account ===")
            print("User Demo: user@example.com / user123")
            print(f"\n=== Sample Game Accounts ===")
            print(f"✅ {len(sample_accounts)} game accounts added to showcase")
            print("✅ Payment settings configured for VietQR")
            print("\nNOTE: Admin passwords are complex and should be changed in production!")
            print("NOTE: Update payment settings in admin panel with real bank info!")
        else:
            print("Database already initialized!")

if __name__ == '__main__':
    init_database()
