#!/usr/bin/env python3
"""
Test startup script locally
"""
import os
from startup import auto_initialize_database

def test_startup():
    """Test the startup script"""
    print("=== Testing Startup Script Locally ===")
    
    # Set environment for testing
    if not os.environ.get('DATABASE_URL'):
        os.environ['DATABASE_URL'] = 'sqlite:///test_startup.db'
        print("Using SQLite for testing")
    
    # Run startup script
    success = auto_initialize_database()
    
    if success:
        print("✅ Startup script test completed successfully!")
    else:
        print("❌ Startup script test failed!")
    
    return success

if __name__ == "__main__":
    test_startup()