#!/usr/bin/env python
"""Simple test to verify app and create test user."""
try:
    from app import app
    from models import User
    from extensions import db
    from werkzeug.security import generate_password_hash
    
    print("✅ App imported successfully")
    
    with app.app_context():
        # Check existing users
        users = User.query.all()
        print(f"📊 Total users: {len(users)}")
        
        # Create test user
        existing = User.query.filter_by(username='testuser').first()
        if existing:
            print("✅ Test user already exists")
        else:
            user = User(
                username='testuser',
                email='test@library.com',
                password=generate_password_hash('TestPass123!'),
                is_admin=True
            )
            db.session.add(user)
            db.session.commit()
            print("✅ Test user created")
        
        print("\n🔐 Login credentials:")
        print("   Username: testuser")
        print("   Password: TestPass123!")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
