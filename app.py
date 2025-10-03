from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import uuid

from extensions import db, login_manager, migrate, cipher_suite, csrf

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Database configuration - Use Render's managed PostgreSQL
database_url = os.environ.get('DATABASE_URL')

if not database_url:
    # Fallback for development
    database_url = 'sqlite:///shop.db'
    print("Using SQLite for development")
else:
    print(f"Using Render PostgreSQL database")

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads/accounts'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
csrf.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Vui lòng đăng nhập để tiếp tục.'

# Import models first so SQLAlchemy knows about them
from models import User, GameAccount, Order, CartItem, AuditLog, Wishlist, PaymentSettings
from forms import LoginForm, RegisterForm, CheckoutForm, AccountForm, PaymentSettingsForm, ForgotPasswordForm, ResetPasswordForm

# Create tables on startup AFTER importing models
with app.app_context():
    try:
        db.create_all()
        print("✅ Database tables created/verified on startup")
        
        # Auto-initialize database if empty
        user_count = User.query.count()
        account_count = GameAccount.query.count()
        
        if user_count == 0 and account_count == 0:
            print("🔄 Database is empty, auto-initializing...")
            from init_db import init_database
            init_database()
            print("🎉 Database auto-initialized with sample data!")
        else:
            print(f"ℹ️ Database has {user_count} users and {account_count} accounts")
            
    except Exception as e:
        print(f"⚠️ Could not create tables on startup: {e}")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_account_image(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        return f"uploads/accounts/{unique_filename}"
    return None

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Vui lòng đăng nhập để tiếp tục.', 'warning')
                return redirect(url_for('login'))
            if not current_user.has_permission(required_role):
                flash('Bạn không có quyền truy cập.', 'danger')
                AuditLog.create_log(current_user.id, 'access_denied', 
                                   f'Attempted to access {request.endpoint} without permission', 
                                   request.remote_addr)
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    try:
        page = request.args.get('page', 1, type=int)
        category = request.args.get('category', '')
        rank = request.args.get('rank', '')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        search = request.args.get('search', '')
        
        query = GameAccount.query.filter_by(is_sold=False)
        
        if category:
            query = query.filter_by(category=category)
        if rank:
            query = query.filter_by(rank=rank)
        if min_price:
            query = query.filter(GameAccount.price >= min_price)
        if max_price:
            query = query.filter(GameAccount.price <= max_price)
        if search:
            query = query.filter(GameAccount.title.ilike(f'%{search}%'))
        
        accounts = query.order_by(GameAccount.created_at.desc()).paginate(
            page=page, per_page=12, error_out=False
        )
        
        categories = db.session.query(GameAccount.category).distinct().all()
        ranks = db.session.query(GameAccount.rank).distinct().all()
        
        return render_template('index.html', 
                             accounts=accounts,
                             categories=[c[0] for c in categories],
                             ranks=[r[0] for r in ranks])
    
    except Exception as e:
        print(f"Database connection error: {e}")
        # Return a maintenance page or basic template
        return render_template('maintenance.html' if os.path.exists('templates/maintenance.html') 
                             else 'index.html', 
                             accounts=None, 
                             categories=[], 
                             ranks=[],
                             db_error=True)

@app.route('/account/<int:account_id>')
def account_detail(account_id):
    account = GameAccount.query.get_or_404(account_id)
    if current_user.is_authenticated:
        AuditLog.create_log(current_user.id, 'view_account', 
                           f'Viewed account {account_id}', request.remote_addr)
    return render_template('account_detail.html', account=account)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            AuditLog.create_log(user.id, 'login', f'User logged in', request.remote_addr)
            next_page = request.args.get('next')
            flash('Đăng nhập thành công!', 'success')
            return redirect(next_page if next_page else url_for('index'))
        else:
            flash('Email hoặc mật khẩu không đúng.', 'danger')
            AuditLog.create_log(None, 'login_failed', 
                               f'Failed login attempt for {form.email.data}', 
                               request.remote_addr)
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            full_name=form.full_name.data,
            phone=form.phone.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        AuditLog.create_log(user.id, 'register', f'New user registered: {user.username}', request.remote_addr)
        flash('Đăng ký thành công! Vui lòng đăng nhập.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    AuditLog.create_log(current_user.id, 'logout', 'User logged out', request.remote_addr)
    logout_user()
    flash('Đã đăng xuất thành công.', 'info')
    return redirect(url_for('index'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            db.session.commit()
            
            reset_url = url_for('reset_password', token=token, _external=True)
            
            flash(f'Link đặt lại mật khẩu: {reset_url}', 'info')
            AuditLog.create_log(user.id, 'password_reset_request', f'Requested password reset', request.remote_addr)
        else:
            flash('Nếu email tồn tại, link đặt lại mật khẩu đã được gửi.', 'info')
        
        return redirect(url_for('login'))
    
    return render_template('forgot_password.html', form=form)

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    user = User.query.filter_by(reset_token=token).first()
    if not user or not user.verify_reset_token(token):
        flash('Link đặt lại mật khẩu không hợp lệ hoặc đã hết hạn.', 'danger')
        return redirect(url_for('forgot_password'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.reset_token = None
        user.reset_token_expiry = None
        db.session.commit()
        
        AuditLog.create_log(user.id, 'password_reset', 'Password reset successful', request.remote_addr)
        flash('Mật khẩu đã được đặt lại thành công! Vui lòng đăng nhập.', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html', form=form, token=token)

@app.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.account.price for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/add_to_cart/<int:account_id>', methods=['POST'])
@login_required
def add_to_cart(account_id):
    account = GameAccount.query.get_or_404(account_id)
    
    if account.is_sold:
        return jsonify({'success': False, 'message': 'Tài khoản đã được bán'}), 400
    
    existing_item = CartItem.query.filter_by(
        user_id=current_user.id,
        account_id=account_id
    ).first()
    
    if existing_item:
        return jsonify({'success': False, 'message': 'Tài khoản đã có trong giỏ hàng'}), 400
    
    cart_item = CartItem(user_id=current_user.id, account_id=account_id)
    db.session.add(cart_item)
    db.session.commit()
    
    AuditLog.create_log(current_user.id, 'add_to_cart', 
                       f'Added account {account_id} to cart', request.remote_addr)
    
    return jsonify({'success': True, 'message': 'Đã thêm vào giỏ hàng'})

@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Không có quyền'}), 403
    
    db.session.delete(cart_item)
    db.session.commit()
    
    AuditLog.create_log(current_user.id, 'remove_from_cart', 
                       f'Removed cart item {item_id}', request.remote_addr)
    
    return jsonify({'success': True, 'message': 'Đã xóa khỏi giỏ hàng'})

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        flash('Giỏ hàng trống.', 'warning')
        return redirect(url_for('cart'))
    
    total = sum(item.account.price for item in cart_items)
    form = CheckoutForm()
    
    if form.validate_on_submit():
        order = Order(
            user_id=current_user.id,
            total_amount=total,
            customer_name=form.customer_name.data,
            customer_email=form.customer_email.data,
            customer_phone=form.customer_phone.data,
            status='pending',
            payment_method='vietqr'
        )
        db.session.add(order)
        db.session.flush()
        
        for cart_item in cart_items:
            cart_item.account.order_id = order.id
            db.session.delete(cart_item)
        
        db.session.commit()
        
        AuditLog.create_log(current_user.id, 'create_order', 
                           f'Created order {order.id} with {len(cart_items)} items, total {total}', 
                           request.remote_addr)
        
        flash('Đơn hàng đã được tạo! Vui lòng quét mã QR để thanh toán.', 'success')
        return redirect(url_for('payment', order_id=order.id))
    
    return render_template('checkout.html', form=form, cart_items=cart_items, total=total)

@app.route('/payment/<int:order_id>')
@login_required
def payment(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('Không có quyền truy cập đơn hàng này.', 'danger')
        return redirect(url_for('orders'))
    
    payment_settings = PaymentSettings.get_active_settings()
    
    if not payment_settings:
        flash('Hệ thống thanh toán chưa được cấu hình. Vui lòng liên hệ quản trị viên.', 'danger')
        return redirect(url_for('order_detail', order_id=order.id))
    
    payment_content = f"DH{order.id}"
    order.payment_reference = payment_content
    db.session.commit()
    
    qr_url = generate_vietqr_url(
        payment_settings.bank_id,
        payment_settings.account_number,
        payment_settings.account_name,
        int(order.total_amount),
        payment_content,
        payment_settings.qr_template
    )
    
    return render_template('payment.html', order=order, qr_url=qr_url, 
                          payment_settings=payment_settings, payment_content=payment_content)

def generate_vietqr_url(bank_id, account_no, account_name, amount, content, template='compact'):
    import urllib.parse
    base_url = f"https://img.vietqr.io/image/{bank_id}-{account_no}-{template}.png"
    params = {
        'amount': amount,
        'addInfo': content,
        'accountName': account_name
    }
    return f"{base_url}?{urllib.parse.urlencode(params)}"

@app.route('/payment/<int:order_id>/confirm', methods=['POST'])
@login_required
def confirm_payment(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.has_permission('support'):
        return jsonify({'success': False, 'message': 'Không có quyền'}), 403
    
    order.status = 'processing'
    db.session.commit()
    
    AuditLog.create_log(current_user.id, 'confirm_payment', 
                       f'Marked payment as sent for order {order.id}', request.remote_addr)
    
    return jsonify({'success': True, 'message': 'Đã xác nhận thanh toán. Vui lòng chờ admin xác nhận.'})

@app.route('/admin/order/<int:order_id>/complete-payment', methods=['POST'])
@role_required('support')
def admin_complete_payment(order_id):
    order = Order.query.get_or_404(order_id)
    
    for account in order.accounts:
        account.is_sold = True
    
    order.status = 'completed'
    db.session.commit()
    
    AuditLog.create_log(current_user.id, 'complete_payment', 
                       f'Completed payment for order {order.id}', request.remote_addr)
    
    return jsonify({'success': True, 'message': 'Đã xác nhận thanh toán thành công'})

@app.route('/orders')
@login_required
def orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=user_orders)

@app.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.has_permission('support'):
        flash('Không có quyền truy cập đơn hàng này.', 'danger')
        AuditLog.create_log(current_user.id, 'access_denied', 
                           f'Attempted to access order {order_id}', request.remote_addr)
        return redirect(url_for('orders'))
    
    if order.status == 'completed':
        AuditLog.create_log(current_user.id, 'view_credentials', 
                           f'Viewed credentials for order {order_id}', request.remote_addr)
    
    return render_template('order_detail.html', order=order)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name')
        current_user.phone = request.form.get('phone')
        db.session.commit()
        AuditLog.create_log(current_user.id, 'update_profile', 
                           'Updated profile information', request.remote_addr)
        flash('Cập nhật thông tin thành công!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('edit_profile.html')

@app.route('/admin')
@role_required('support')
def admin_dashboard():
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).filter_by(status='completed').scalar() or 0
    total_accounts = GameAccount.query.count()
    sold_accounts = GameAccount.query.filter_by(is_sold=True).count()
    pending_orders = Order.query.filter_by(status='pending').count()
    
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html',
                         total_revenue=total_revenue,
                         total_accounts=total_accounts,
                         sold_accounts=sold_accounts,
                         pending_orders=pending_orders,
                         recent_orders=recent_orders)

@app.route('/admin/accounts')
@role_required('support')
def admin_accounts():
    page = request.args.get('page', 1, type=int)
    accounts = GameAccount.query.order_by(GameAccount.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/accounts.html', accounts=accounts)

@app.route('/admin/account/add', methods=['GET', 'POST'])
@role_required('admin')
def admin_add_account():
    form = AccountForm()
    if form.validate_on_submit():
        encrypted_username = cipher_suite.encrypt(form.account_username.data.encode()).decode()
        encrypted_password = cipher_suite.encrypt(form.account_password.data.encode()).decode()
        
        account = GameAccount(
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            rank=form.rank.data,
            price=form.price.data,
            account_username=encrypted_username,
            account_password=encrypted_password,
            internal_notes=form.internal_notes.data,
            images=[]
        )
        
        if form.images.data:
            for image_file in form.images.data:
                if image_file and image_file.filename:
                    image_path = save_account_image(image_file)
                    if image_path:
                        account.add_image(image_path)
        
        db.session.add(account)
        db.session.commit()
        
        AuditLog.create_log(current_user.id, 'create_account', 
                           f'Created account {account.id}: {account.title}', request.remote_addr)
        
        flash('Đã thêm tài khoản thành công!', 'success')
        return redirect(url_for('admin_accounts'))
    
    return render_template('admin/account_form.html', form=form, action='add')

@app.route('/admin/account/edit/<int:account_id>', methods=['GET', 'POST'])
@role_required('admin')
def admin_edit_account(account_id):
    account = GameAccount.query.get_or_404(account_id)
    
    if request.method == 'GET':
        form = AccountForm(
            title=account.title,
            description=account.description,
            category=account.category,
            rank=account.rank,
            price=account.price,
            internal_notes=account.internal_notes
        )
    else:
        form = AccountForm()
    
    if form.validate_on_submit():
        account.title = form.title.data
        account.description = form.description.data
        account.category = form.category.data
        account.rank = form.rank.data
        account.price = form.price.data
        account.internal_notes = form.internal_notes.data
        
        if form.account_username.data and form.account_username.data.strip():
            account.account_username = cipher_suite.encrypt(form.account_username.data.encode()).decode()
        if form.account_password.data and form.account_password.data.strip():
            account.account_password = cipher_suite.encrypt(form.account_password.data.encode()).decode()
        
        if form.images.data:
            for image_file in form.images.data:
                if image_file and image_file.filename:
                    image_path = save_account_image(image_file)
                    if image_path:
                        account.add_image(image_path)
        
        db.session.commit()
        
        AuditLog.create_log(current_user.id, 'edit_account', 
                           f'Edited account {account.id}: {account.title}', request.remote_addr)
        
        flash('Đã cập nhật tài khoản thành công!', 'success')
        return redirect(url_for('admin_accounts'))
    
    decrypted_username = account.get_decrypted_username()
    decrypted_password = account.get_decrypted_password()
    
    return render_template('admin/account_form.html', form=form, action='edit', account=account,
                          decrypted_username=decrypted_username, decrypted_password=decrypted_password)

@app.route('/admin/account/delete/<int:account_id>', methods=['POST'])
@role_required('admin')
def admin_delete_account(account_id):
    account = GameAccount.query.get_or_404(account_id)
    
    if account.is_sold:
        return jsonify({'success': False, 'message': 'Không thể xóa tài khoản đã bán'}), 400
    
    AuditLog.create_log(current_user.id, 'delete_account', 
                       f'Deleted account {account.id}: {account.title}', request.remote_addr)
    
    db.session.delete(account)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Đã xóa tài khoản'})

@app.route('/admin/orders')
@role_required('support')
def admin_orders():
    page = request.args.get('page', 1, type=int)
    orders = Order.query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/orders.html', orders=orders)

@app.route('/admin/order/<int:order_id>/update_status', methods=['POST'])
@role_required('support')
def admin_update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.json.get('status')
    
    if new_status not in ['pending', 'processing', 'completed', 'cancelled']:
        return jsonify({'success': False, 'message': 'Trạng thái không hợp lệ'}), 400
    
    old_status = order.status
    order.status = new_status
    db.session.commit()
    
    AuditLog.create_log(current_user.id, 'update_order_status', 
                       f'Updated order {order.id} status from {old_status} to {new_status}', 
                       request.remote_addr)
    
    return jsonify({'success': True, 'message': 'Đã cập nhật trạng thái'})

@app.route('/admin/logs')
@role_required('admin')
def admin_logs():
    page = request.args.get('page', 1, type=int)
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).paginate(
        page=page, per_page=50, error_out=False
    )
    return render_template('admin/logs.html', logs=logs)

@app.route('/admin/payment-settings', methods=['GET', 'POST'])
@role_required('admin')
def admin_payment_settings():
    settings = PaymentSettings.get_active_settings()
    
    if request.method == 'GET':
        if settings:
            form = PaymentSettingsForm(
                bank_id=settings.bank_id,
                bank_name=settings.bank_name,
                account_number=settings.account_number,
                account_name=settings.account_name,
                qr_template=settings.qr_template
            )
        else:
            form = PaymentSettingsForm()
    else:
        form = PaymentSettingsForm()
    
    if form.validate_on_submit():
        if settings:
            settings.bank_id = form.bank_id.data
            settings.bank_name = form.bank_name.data
            settings.account_number = form.account_number.data
            settings.account_name = form.account_name.data
            settings.qr_template = form.qr_template.data
            flash_msg = 'Đã cập nhật cài đặt thanh toán!'
        else:
            settings = PaymentSettings(
                bank_id=form.bank_id.data,
                bank_name=form.bank_name.data,
                account_number=form.account_number.data,
                account_name=form.account_name.data,
                qr_template=form.qr_template.data,
                is_active=True
            )
            db.session.add(settings)
            flash_msg = 'Đã thêm cài đặt thanh toán!'
        
        db.session.commit()
        
        AuditLog.create_log(current_user.id, 'update_payment_settings', 
                           f'Updated VietQR payment settings', request.remote_addr)
        
        flash(flash_msg, 'success')
        return redirect(url_for('admin_payment_settings'))
    
    return render_template('admin/payment_settings.html', form=form, settings=settings)

@app.route('/wishlist')
@login_required
def wishlist():
    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
    return render_template('wishlist.html', wishlist_items=wishlist_items)

@app.route('/wishlist/add/<int:account_id>', methods=['POST'])
@login_required
def add_to_wishlist(account_id):
    account = GameAccount.query.get_or_404(account_id)
    
    if account.is_sold:
        return jsonify({'success': False, 'message': 'Tài khoản đã được bán'}), 400
    
    existing = Wishlist.query.filter_by(user_id=current_user.id, account_id=account_id).first()
    if existing:
        return jsonify({'success': False, 'message': 'Đã có trong danh sách yêu thích'}), 400
    
    wishlist_item = Wishlist(user_id=current_user.id, account_id=account_id)
    db.session.add(wishlist_item)
    db.session.commit()
    
    AuditLog.create_log(current_user.id, 'add_to_wishlist', 
                       f'Added account {account_id} to wishlist', request.remote_addr)
    
    return jsonify({'success': True, 'message': 'Đã thêm vào danh sách yêu thích'})

@app.route('/wishlist/remove/<int:account_id>', methods=['POST'])
@login_required
def remove_from_wishlist(account_id):
    wishlist_item = Wishlist.query.filter_by(user_id=current_user.id, account_id=account_id).first_or_404()
    
    db.session.delete(wishlist_item)
    db.session.commit()
    
    AuditLog.create_log(current_user.id, 'remove_from_wishlist', 
                       f'Removed account {account_id} from wishlist', request.remote_addr)
    
    return jsonify({'success': True, 'message': 'Đã xóa khỏi danh sách yêu thích'})

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Test database connection
        with db.engine.connect() as connection:
            connection.execute(db.text('SELECT 1'))
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/status')
def status():
    """Simple status page"""
    return render_template('status.html')

@app.route('/init-db')
def init_database_route():
    """Initialize database tables and data"""
    try:
        # Create all tables
        db.create_all()
        
        # Check if we need to initialize data
        user_count = User.query.count()
        account_count = GameAccount.query.count()
        
        if user_count == 0:
            from init_db import init_database
            init_database()
            return jsonify({
                'status': 'success',
                'message': 'Database initialized with sample data',
                'users_created': User.query.count(),
                'accounts_created': GameAccount.query.count()
            })
        else:
            return jsonify({
                'status': 'success', 
                'message': f'Database already has {user_count} users and {account_count} accounts',
                'users_count': user_count,
                'accounts_count': account_count
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/reset-db')
def reset_database_route():
    """Reset database and reinitialize with sample data"""
    try:
        # Drop all tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        # Initialize with sample data
        from init_db import init_database
        init_database()
        
        return jsonify({
            'status': 'success',
            'message': 'Database reset and initialized successfully',
            'users_created': User.query.count(),
            'accounts_created': GameAccount.query.count()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/startup-status')
def startup_status():
    """Check startup and database status"""
    try:
        user_count = User.query.count()
        account_count = GameAccount.query.count()
        payment_count = PaymentSettings.query.count()
        
        return jsonify({
            'status': 'success',
            'database_status': 'connected',
            'users': user_count,
            'accounts': account_count,
            'payment_settings': payment_count,
            'initialized': user_count > 0 and account_count > 0,
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'database_status': 'disconnected',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/force-init')
def force_init():
    """Force initialize database with sample data"""
    try:
        # Always run initialization
        from init_db import init_database
        
        # Drop and recreate tables
        db.drop_all()
        db.create_all()
        
        # Initialize with sample data
        init_database()
        
        return jsonify({
            'status': 'success',
            'message': 'Database force initialized successfully',
            'users_created': User.query.count(),
            'accounts_created': GameAccount.query.count(),
            'payment_settings_created': PaymentSettings.query.count()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
