#!/usr/bin/env python3
"""
Script to check Supabase connection from Render environment
"""
import os
import socket
import time
from database_config import test_connection, get_database_url

def check_network_connectivity():
    """Check if we can reach Supabase host"""
    host = "db.iohaxfkciqvcoxsvzfyh.supabase.co"
    port = 5432
    timeout = 10
    
    try:
        print(f"Testing network connectivity to {host}:{port}...")
        sock = socket.create_connection((host, port), timeout)
        sock.close()
        print("✅ Network connectivity OK")
        return True
    except Exception as e:
        print(f"❌ Network connectivity failed: {e}")
        return False

def check_dns_resolution():
    """Check DNS resolution for Supabase host"""
    host = "db.iohaxfkciqvcoxsvzfyh.supabase.co"
    
    try:
        print(f"Testing DNS resolution for {host}...")
        ip = socket.gethostbyname(host)
        print(f"✅ DNS resolution OK: {host} -> {ip}")
        return True
    except Exception as e:
        print(f"❌ DNS resolution failed: {e}")
        return False

def main():
    print("=== Supabase Connection Diagnostics ===")
    print(f"Environment: {os.environ.get('RENDER', 'Local')}")
    print(f"Python version: {os.sys.version}")
    
    # Check DNS
    dns_ok = check_dns_resolution()
    
    # Check network connectivity
    network_ok = check_network_connectivity()
    
    # Check database connection
    if dns_ok and network_ok:
        print("\nTesting database connection...")
        db_url = get_database_url()
        db_ok = test_connection(db_url)
        
        if db_ok:
            print("✅ All checks passed! Supabase connection is working.")
        else:
            print("❌ Database connection failed despite network connectivity.")
    else:
        print("❌ Network issues detected. Cannot test database connection.")
    
    print("\n=== Diagnostic Complete ===")

if __name__ == "__main__":
    main()