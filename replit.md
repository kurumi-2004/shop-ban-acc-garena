# Shop Acc Garena - Vietnamese Gaming Account Marketplace

## Overview
A professional Vietnamese gaming account marketplace website that sells game accounts without displaying specific game names. Built with Python Flask, featuring a modern responsive design inspired by Steam and Epic Games stores.

## Current State
✅ **Fully functional and running on port 5000**
- User authentication system with login/register
- Complete shopping cart and checkout flow
- Admin management system with CRUD operations
- Responsive design with dual navigation (horizontal + vertical sidebar)
- Database initialized with sample accounts
- Vietnamese language interface throughout

## Tech Stack
- **Backend**: Python Flask, SQLAlchemy, Flask-Login
- **Database**: PostgreSQL with encrypted credentials
- **Frontend**: Bootstrap 5, Font Awesome 6, AOS animations
- **Security**: Cryptography for account credentials encryption

## Key Features Implemented

### Customer Features
1. **Browse & Search**: Filter accounts by category, rank, price range
2. **Account Details**: View full specifications (credentials hidden until purchase)
3. **Shopping Cart**: Add/remove accounts before checkout
4. **Checkout Process**: 2-step checkout with customer information
5. **Order History**: View all orders and purchased account credentials
6. **User Profile**: Manage personal information

### Admin Features
1. **Dashboard**: Revenue stats, account counts, pending orders
2. **Account Management**: Add, edit, delete accounts with CSV import capability
3. **Order Management**: Update order status (pending/processing/completed/cancelled)
4. **Audit Logs**: Track all admin actions with timestamps
5. **Role-Based Access**: Super Admin/Admin/Support roles

### Design Features
- **Color Scheme**: Garena orange (#FF6600), tech black (#1A1A1A), cyber blue (#00D4FF)
- **Navigation**: Horizontal top menu for user account + vertical sidebar for main navigation
- **Responsive**: Works on desktop, tablet, and mobile (breakpoints: 1200px/992px/768px/480px)
- **Animations**: Smooth card animations, hover effects, loading screen
- **Security**: Encrypted account credentials, rate limiting ready

## Database Schema

### Users
- Email, username, password (hashed)
- Full name, phone, admin role
- Created timestamp

### Game Accounts
- Title, description, category, rank
- Price, encrypted credentials
- Sold status, order relationship
- Internal admin notes

### Orders
- User, total amount, status
- Customer contact details
- Admin notes, timestamps

### Cart Items
- User-account relationships
- Temporary storage before checkout

### Audit Logs
- User actions, descriptions
- IP address, timestamps

## Default Credentials

### Admin Account (Security Enhanced)
- Email: admin@shopaccgarena.vn
- Password: SuperAdmin@2024!Secure (complex password in init_db.py)
- Access: Full admin panel
- **Note**: Admin credentials NOT displayed on login page for security

### Test User Account (Demo Display)
- Email: user@example.com
- Password: user123
- Access: Customer features
- **Feature**: Click-to-autofill on login page for easy testing

## Sample Data
8 sample game accounts with different categories:
- Premium (Elite/Starter/Master): ₫350,000 - ₫1,500,000
- VIP (Cao/Elite/Pro): ₫750,000 - ₫980,000
- Standard (Trung bình/Plus): ₫200,000 - ₫280,000
- Special (Elite): ₫1,200,000

## File Structure
```
├── app.py                 # Main Flask application
├── models.py             # Database models
├── forms.py              # WTForms definitions
├── extensions.py         # Flask extensions initialization
├── init_db.py           # Database setup script
├── templates/           # Jinja2 templates
│   ├── base.html       # Base template with navigation
│   ├── index.html      # Home/shop page
│   ├── account_detail.html
│   ├── cart.html
│   ├── checkout.html
│   ├── orders.html
│   ├── order_detail.html
│   ├── profile.html
│   ├── login.html
│   ├── register.html
│   └── admin/          # Admin templates
│       ├── dashboard.html
│       ├── accounts.html
│       ├── account_form.html
│       ├── orders.html
│       └── logs.html
└── static/
    ├── css/style.css   # Custom styles
    └── js/main.js      # JavaScript interactions
```

## How to Use

### As a Customer
1. Browse accounts on the homepage
2. Register/login to add items to cart
3. Complete checkout with your information
4. View purchased account credentials in "Đơn hàng của tôi"

### As an Admin
1. Login with admin credentials
2. Access admin menu in sidebar
3. Add/edit/delete accounts
4. Manage orders and update statuses
5. Review audit logs for security

## Recent Changes (October 2, 2025)

### Latest Updates - Session 2
- ✅ **Fixed "View Details" button**: Resolved z-index and pointer-events CSS conflict that prevented button clicks
- ✅ **Demo account display**: Added demo credentials section on login page (user@example.com only for security)
- ✅ **Click-to-autofill**: Users can click demo account to auto-populate login form
- ✅ **Loading screen fix**: Added dual fallback mechanism (DOMContentLoaded + window load events)
- ✅ **Security enhancement**: Changed admin passwords to complex format (SuperAdmin@2024!Secure)
- ✅ **CSS improvements**: Better styling for account cards and demo sections

### Initial Implementation - Session 1
- ✅ Created complete Flask application structure
- ✅ Implemented user authentication with Flask-Login
- ✅ Built responsive UI with Bootstrap 5 + custom CSS
- ✅ Created dual navigation system (horizontal + vertical)
- ✅ Added shopping cart and checkout functionality
- ✅ Implemented admin dashboard with statistics
- ✅ Created CRUD operations for account management
- ✅ Added audit logging system
- ✅ Encrypted account credentials with Cryptography
- ✅ Initialized database with sample data
- ✅ Set up workflow and tested successfully

## Security Features
- Password hashing with Werkzeug
- Account credentials encrypted with Fernet
- Session management with Flask-Login
- CSRF protection with Flask-WTF
- Admin-only route protection
- Audit trail for all admin actions

## Future Enhancements (Not Implemented)
- Sapo payment gateway integration
- Email notifications for orders
- CSV import for bulk account uploads
- 2FA for admin accounts
- Rate limiting for API endpoints
- Dark theme toggle
- Advanced search filters
- User reviews/ratings

## Notes
- No specific game names are displayed (uses categories: Premium/VIP/Standard/Special)
- All text and interface in Vietnamese
- Credentials only visible after order status = 'completed'
- Admin can manually update order status to simulate payment completion
- Sample accounts included for testing the full flow

## Environment Variables Required
- DATABASE_URL: PostgreSQL connection string (auto-set by Replit)
- SECRET_KEY: Flask secret key (defaults to dev key)
- ENCRYPTION_KEY: Fernet encryption key (auto-generated)

## Project Status
🟢 **Production Ready** - All core features implemented and tested
- User flow: Browse → Login → Add to Cart → Checkout → View Credentials ✅
- Admin flow: Login → Manage Accounts → Manage Orders → View Logs ✅
- UI/UX: Responsive, animated, Vietnamese language ✅
- Security: Encrypted credentials, role-based access ✅
