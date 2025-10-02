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
            
            db.session.commit()
            print("User accounts added successfully!")
            print("\n=== IMPORTANT: Admin Credentials (DO NOT SHARE) ===")
            print("\nSuper Admin: superadmin@shopaccgarena.vn / SuperAdmin@2024!Secure")
            print("Admin: admin@shopaccgarena.vn / Admin@2024!Secure")
            print("Support: support@shopaccgarena.vn / Support@2024!Secure")
            print("\n=== Public Demo Account ===")
            print("User Demo: user@example.com / user123")
            print("\nNOTE: Admin passwords are complex and should be changed in production!")
            print("NOTE: No sample game accounts added. Please add accounts via admin panel.")
        else:
            print("Database already initialized!")

if __name__ == '__main__':
    init_database()
