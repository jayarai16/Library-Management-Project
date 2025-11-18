#!/usr/bin/env python
"""Test registration and create a working test user."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Check existing users
    users = User.query.all()
    print(f"Total users in database: {len(users)}")
    for u in users:
        print(f"  - {u.username} ({u.email})")
    
    # Create a test user if doesn't exist
    test_user = User.query.filter_by(username='testuser').first()
    if not test_user:
        print("\nCreating test user...")
        user = User(
            username='testuser',
            email='test@library.com',
            password=generate_password_hash('TestPass123!'),
            is_admin=True
        )
        from extensions import db
        db.session.add(user)
        db.session.commit()
        print("✅ Test user created!")
    else:
        print("\n✅ Test user already exists!")
    
    print("\n📝 Credentials:")
    print("   Username: testuser")
    print("   Password: TestPass123!")
