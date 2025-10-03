#!/usr/bin/env bash
# Build script for Render

set -o errexit

pip install -r requirements.txt

# Initialize database
python init_db.py
