"""Fill missing book cover images by querying Open Library.
Backs up instance/library.db before making changes.

Run: python fill_missing_images.py
"""
import os
import time
import shutil
import requests

from app import app
from extensions import db
from models import Book

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'library.db')
BACKUP_DIR = os.path.join(BASE_DIR, 'backups')
os.makedirs(BACKUP_DIR, exist_ok=True)

def backup_db():
    ts = time.strftime('%Y%m%d_%H%M%S')
    dest = os.path.join(BACKUP_DIR, f'instance_library.db.bak.images.{ts}')
    if os.path.exists(DB_PATH):
        shutil.copy2(DB_PATH, dest)
        print(f'Backup created: {dest}')
    else:
        print('Instance DB not found at', DB_PATH)


def fetch_by_isbn(isbn):
    isbn_clean = isbn.replace('-', '').strip()
    if not isbn_clean:
        return None
    url = f'https://covers.openlibrary.org/b/isbn/{isbn_clean}-L.jpg'
    try:
        r = requests.head(url, timeout=6)
        if r.status_code == 200:
            return url
    except Exception:
        pass
    return None


def fetch_by_search(title, author):
    # Use Open Library search API to try to find a cover id
    q = []
    if title:
        q.append(f'title={requests.utils.quote(title)}')
    if author:
        q.append(f'author={requests.utils.quote(author)}')
    if not q:
        return None
    url = 'https://openlibrary.org/search.json?' + '&'.join(q)
    try:
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            data = r.json()
            docs = data.get('docs') or []
            if docs:
                # Prefer cover_i if available
                for d in docs:
                    cover_i = d.get('cover_i')
                    if cover_i:
                        return f'https://covers.openlibrary.org/b/id/{cover_i}-L.jpg'
                # Fallback to ISBN from doc
                for d in docs:
                    isbns = d.get('isbn') or []
                    if isbns:
                        isbn0 = isbns[0]
                        res = fetch_by_isbn(isbn0)
                        if res:
                            return res
    except Exception:
        pass
    return None


def main():
    backup_db()
    updated = 0
    tried = 0
    with app.app_context():
        books = Book.query.filter((Book.image_url == None) | (Book.image_url == '')).all()
        print('Books missing images:', len(books))
        for b in books:
            tried += 1
            print(f'[{tried}/{len(books)}] Trying: {b.title} by {b.author} (ISBN: {b.isbn})')
            img = None
            if b.isbn:
                img = fetch_by_isbn(b.isbn)
            if not img:
                img = fetch_by_search(b.title, b.author)
            if img:
                b.image_url = img
                db.session.add(b)
                updated += 1
                print('  -> Found image:', img)
            else:
                print('  -> No image found')
        if updated:
            db.session.commit()
    print(f'Done. Updated {updated} book(s) with images.')


if __name__ == '__main__':
    main()
