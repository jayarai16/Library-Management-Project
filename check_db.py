#!/usr/bin/env python
"""Check database and seed if needed."""
import os
import sys

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from extensions import db
from models import Book, User

with app.app_context():
    # Check books count
    book_count = Book.query.count()
    user_count = User.query.count()
    
    print(f"Total books in DB: {book_count}")
    print(f"Total users in DB: {user_count}")
    
    if book_count == 0:
        print("\nNo books found. Running init_db script...")
        exec(open('init_db.py').read())
    else:
        print(f"\nBooks found! First 5 books:")
        books = Book.query.limit(5).all()
        for b in books:
            print(f"  - {b.title} by {b.author} (Available: {b.get_available_count()}/{b.quantity})")
