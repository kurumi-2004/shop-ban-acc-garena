from extensions import db, cipher_suite
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    orders = db.relationship('Order', backref='user', lazy='dynamic')
    cart_items = db.relationship('CartItem', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    wishlist_items = db.relationship('Wishlist', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def has_permission(self, required_role):
        role_hierarchy = {'user': 0, 'support': 1, 'admin': 2, 'superadmin': 3}
        user_level = role_hierarchy.get(self.role, 0)
        required_level = role_hierarchy.get(required_role, 0)
        return user_level >= required_level
    
    def __repr__(self):
        return f'<User {self.username}>'

class GameAccount(db.Model):
    __tablename__ = 'game_accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100), nullable=False, index=True)
    rank = db.Column(db.String(50))
    price = db.Column(db.Float, nullable=False)
    account_username = db.Column(db.Text, nullable=False)
    account_password = db.Column(db.Text, nullable=False)
    is_sold = db.Column(db.Boolean, default=False, index=True)
    internal_notes = db.Column(db.Text)
    images = db.Column(db.JSON, default=list)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    
    def get_decrypted_username(self):
        try:
            return cipher_suite.decrypt(self.account_username.encode()).decode()
        except Exception:
            return '[Lỗi giải mã]'
    
    def get_decrypted_password(self):
        try:
            return cipher_suite.decrypt(self.account_password.encode()).decode()
        except Exception:
            return '[Lỗi giải mã]'
    
    def get_images(self):
        if self.images:
            return self.images
        return []
    
    def add_image(self, image_path):
        if self.images is None:
            self.images = []
        if isinstance(self.images, list):
            self.images.append(image_path)
        else:
            self.images = [image_path]
    
    def remove_image(self, image_path):
        if self.images and isinstance(self.images, list) and image_path in self.images:
            self.images.remove(image_path)
    
    def __repr__(self):
        return f'<GameAccount {self.title}>'

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending', index=True)
    customer_name = db.Column(db.String(120), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(20))
    payment_method = db.Column(db.String(50), default='vietqr')
    payment_reference = db.Column(db.String(200))
    admin_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    accounts = db.relationship('GameAccount', backref='order', lazy='dynamic')
    
    def __repr__(self):
        return f'<Order {self.id}>'

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('game_accounts.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    account = db.relationship('GameAccount', backref='cart_items')
    
    def __repr__(self):
        return f'<CartItem {self.id}>'

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    ip_address = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    user = db.relationship('User', backref='audit_logs')
    
    @staticmethod
    def create_log(user_id, action, description, ip_address=None):
        log = AuditLog(
            user_id=user_id,
            action=action,
            description=description,
            ip_address=ip_address
        )
        db.session.add(log)
        db.session.commit()
        return log
    
    def __repr__(self):
        return f'<AuditLog {self.action}>'

class Wishlist(db.Model):
    __tablename__ = 'wishlists'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('game_accounts.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    account = db.relationship('GameAccount', backref='wishlist_items')
    
    def __repr__(self):
        return f'<Wishlist {self.id}>'

class PaymentSettings(db.Model):
    __tablename__ = 'payment_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    bank_id = db.Column(db.String(20), nullable=False)
    bank_name = db.Column(db.String(100), nullable=False)
    account_number = db.Column(db.String(50), nullable=False)
    account_name = db.Column(db.String(200), nullable=False)
    qr_template = db.Column(db.String(20), default='compact')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @staticmethod
    def get_active_settings():
        return PaymentSettings.query.filter_by(is_active=True).first()
    
    def __repr__(self):
        return f'<PaymentSettings {self.bank_name}>'
