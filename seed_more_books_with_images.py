"""Seed more books into the instance database, including image_url when possible.
This script will add books only if their ISBN does not already exist in the database.
Run: python seed_more_books_with_images.py
"""

from app import app
from extensions import db
from models import Book
import requests

# A small curated list of books with ISBNs. We'll attempt to fetch cover images via Open Library.
books_to_add = [
    {"title": "Inferno", "author": "Dan Brown", "isbn": "9781400079155", "publication_year": 2013, "quantity": 4, "description": "A thriller about a Dante-related mystery."},
    {"title": "The Girl on the Train", "author": "Paula Hawkins", "isbn": "9781594633669", "publication_year": 2015, "quantity": 5, "description": "A psychological thriller."},
    {"title": "The Little Prince", "author": "Antoine de Saint-Exupéry", "isbn": "9780156012195", "publication_year": 1943, "quantity": 6, "description": "A poetic tale about a young prince."},
    {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "isbn": "9780316769488", "publication_year": 1951, "quantity": 3, "description": "A classic coming-of-age novel."},
    {"title": "Percy Jackson & the Olympians: The Lightning Thief", "author": "Rick Riordan", "isbn": "9780786838653", "publication_year": 2005, "quantity": 6, "description": "A modern-day mythic adventure."},
]

def fetch_cover(isbn):
    """Try to get a cover image URL from Open Library covers API."""
    try:
        # Open Library cover endpoint (small/medium/large). Use large for better quality.
        url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
        # Quick HEAD to check if exists (returns 200)
        r = requests.head(url, timeout=5)
        if r.status_code == 200:
            return url
    except Exception:
        pass
    return None


def add_books():
    added = 0
    with app.app_context():
        for b in books_to_add:
            isbn_clean = b['isbn'].replace('-', '').strip()
            existing = Book.query.filter_by(isbn=b['isbn']).first()
            if existing:
                print(f"Skipping existing book: {b['title']} ({b['isbn']})")
                continue

            image = fetch_cover(isbn_clean)

            book = Book(
                title=b['title'],
                author=b['author'],
                isbn=b['isbn'],
                publication_year=b['publication_year'],
                quantity=b.get('quantity', 1),
                available=True,
                description=b.get('description', ''),
                image_url=image
            )
            db.session.add(book)
            added += 1
        if added:
            db.session.commit()
        print(f"Done. {added} new book(s) added.")


if __name__ == '__main__':
    add_books()
