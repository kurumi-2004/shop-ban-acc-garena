# Supabase Integration Guide

## Overview
This Flask e-commerce application now supports Supabase integration with both PostgreSQL database and Supabase API features.

## Database Configuration

### PostgreSQL Connection
- **Database URL**: `postgresql://postgres:[password]@db.iohaxfkciqvcoxsvzfyh.supabase.co:5432/postgres`
- **Supabase Project**: `iohaxfkciqvcoxsvzfyh`
- **Region**: Auto-selected by Supabase

### Supabase API
- **URL**: `https://iohaxfkciqvcoxsvzfyh.supabase.co`
- **API Key**: Configured in environment variables

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Variables
Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

Update the following variables:
- `DATABASE_URL`: PostgreSQL connection string
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase anon public key
- `SECRET_KEY`: Flask secret key
- `ENCRYPTION_KEY`: For encrypting sensitive data

### 3. Initialize Database
```bash
python init_db.py
```

### 4. Test Connections
```bash
python test_supabase.py
```

## Features

### Database Models
- **Users**: User authentication and profiles
- **GameAccounts**: Game accounts for sale
- **Orders**: Purchase orders
- **CartItems**: Shopping cart functionality
- **AuditLog**: System activity logging
- **Wishlist**: User wishlist feature
- **PaymentSettings**: VietQR payment configuration

### Admin Accounts
After running `init_db.py`, the following accounts are created:

**Super Admin**
- Email: `superadmin@shopaccgarena.vn`
- Password: `SuperAdmin@2024!Secure`

**Admin**
- Email: `admin@shopaccgarena.vn`
- Password: `Admin@2024!Secure`

**Support**
- Email: `support@shopaccgarena.vn`
- Password: `Support@2024!Secure`

**Demo User**
- Email: `user@example.com`
- Password: `user123`

### Supabase Features
- Real-time data synchronization
- Row Level Security (RLS)
- API integration for advanced features
- Backup and monitoring through Supabase dashboard

## Deployment

### Railway
Configuration in `railway.toml`:
```toml
[build]
builder = "nixpacks"

[deploy]
healthcheckPath = "/"
healthcheckTimeout = 300
restartPolicyType = "on_failure"
```

### Render
Configuration in `render.yaml` with automatic database and environment setup.

## Security Notes

1. **Change default passwords** in production
2. **Use environment variables** for sensitive data
3. **Enable RLS** in Supabase for additional security
4. **Regular backups** through Supabase dashboard

## Troubleshooting

### Connection Issues
1. Verify database URL and credentials
2. Check Supabase project status
3. Ensure firewall allows connections
4. Test with `python test_supabase.py`

### API Key Issues
1. Get fresh API key from Supabase dashboard
2. Update `SUPABASE_KEY` environment variable
3. Restart application

## Support
For issues related to this integration, check:
1. Supabase dashboard logs
2. Application logs
3. Database connection status
4. API key validity

## Version History
- **v1.0**: Initial Supabase integration
- **v1.1**: Added comprehensive testing and documentation