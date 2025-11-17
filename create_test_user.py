#!/usr/bin/env python
"""Create a test user for quick login."""
import os
import sys
from werkzeug.security import generate_password_hash

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from extensions import db
from models import User

with app.app_context():
    # Check if user already exists
    existing = User.query.filter_by(username='testuser').first()
    if existing:
        print("Test user 'testuser' already exists!")
        print("Username: testuser")
        print("Password: test123")
    else:
        # Create test user
        user = User(
            username='testuser',
            email='test@library.com',
            password=generate_password_hash('test123'),
            is_admin=True
        )
        db.session.add(user)
        db.session.commit()
        print("✅ Test user created!")
        print("Username: testuser")
        print("Password: test123")
        print("(This user is an admin)")
