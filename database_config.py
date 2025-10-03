#!/usr/bin/env python3
"""
Database configuration with connection pooling and retry logic for Supabase
"""
import os
import time
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_supabase_engine(max_retries=3, retry_delay=2):
    """
    Create SQLAlchemy engine with connection pooling for Supabase
    """
    # Supabase connection parameters
    supabase_url = "postgresql+pg8000://postgres:25862586a@db.iohaxfkciqvcoxsvzfyh.supabase.co:5432/postgres"
    
    # Connection pool configuration
    engine_config = {
        'poolclass': QueuePool,
        'pool_size': 5,
        'max_overflow': 10,
        'pool_pre_ping': True,
        'pool_recycle': 300,  # 5 minutes
        'connect_args': {
            'connect_timeout': 10,
            'application_name': 'shop-ban-acc-garena'
        }
    }
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting to connect to Supabase (attempt {attempt + 1}/{max_retries})")
            
            engine = create_engine(supabase_url, **engine_config)
            
            # Test connection
            with engine.connect() as conn:
                result = conn.execute(text('SELECT 1'))
                logger.info("✅ Successfully connected to Supabase!")
                return engine
                
        except Exception as e:
            logger.error(f"❌ Connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error("All connection attempts failed!")
                raise
    
    return None

def get_database_url():
    """
    Get the appropriate database URL with fallback options
    """
    # Check environment variable first
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url and 'supabase.co' not in database_url:
        # Use provided URL (e.g., from Render)
        logger.info("Using provided DATABASE_URL")
        return database_url
    
    # Use Supabase as primary option
    supabase_url = "postgresql+pg8000://postgres:25862586a@db.iohaxfkciqvcoxsvzfyh.supabase.co:5432/postgres"
    logger.info("Using Supabase database URL")
    return supabase_url

def test_connection(database_url):
    """
    Test database connection
    """
    try:
        engine = create_engine(database_url, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text('SELECT 1'))
        return True
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        return False

if __name__ == "__main__":
    # Test the connection
    url = get_database_url()
    print(f"Testing connection to: {url[:50]}...")
    
    if test_connection(url):
        print("✅ Database connection successful!")
    else:
        print("❌ Database connection failed!")