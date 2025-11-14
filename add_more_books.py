"""
Add a larger, diverse set of books to the existing database.
This script will add books only if their ISBN does not already exist in the database.
Run: python add_more_books.py
"""

from app import app
from extensions import db
from models import Book

books_to_add = [
    {"title": "The Alchemist", "author": "Paulo Coelho", "isbn": "978-0061122415", "publication_year": 1988, "quantity": 5, "description": "A philosophical story about following your dreams."},
    {"title": "The Alchemist", "author": "Paulo Coelho", "isbn": "978-0061122415", "publication_year": 1988, "quantity": 5, "description": "A philosophical story about following your dreams.", "image_url": "https://covers.openlibrary.org/b/isbn/9780061122415-L.jpg"},
    {"title": "Sapiens: A Brief History of Humankind", "author": "Yuval Noah Harari", "isbn": "978-0062316097", "publication_year": 2011, "quantity": 4, "description": "Historical exploration of humanity's development."},
    {"title": "Atomic Habits", "author": "James Clear", "isbn": "978-0735211292", "publication_year": 2018, "quantity": 6, "description": "Practical strategies to build good habits and break bad ones."},
    {"title": "Educated", "author": "Tara Westover", "isbn": "978-0399590504", "publication_year": 2018, "quantity": 3, "description": "A memoir about a woman who grows up in a survivalist family and goes on to earn a PhD."},
    {"title": "The Silent Patient", "author": "Alex Michaelides", "isbn": "978-1250301697", "publication_year": 2019, "quantity": 2, "description": "A psychological thriller about a woman who stops speaking after a violent act."},
    {"title": "Becoming", "author": "Michelle Obama", "isbn": "978-1524763138", "publication_year": 2018, "quantity": 4, "description": "The former First Lady's memoir."},
    {"title": "The Road", "author": "Cormac McCarthy", "isbn": "978-0307387899", "publication_year": 2006, "quantity": 2, "description": "A post-apocalyptic novel about a father and son."},
    {"title": "Dune", "author": "Frank Herbert", "isbn": "978-0441013593", "publication_year": 1965, "quantity": 5, "description": "Epic science fiction novel set on the desert planet Arrakis."},
    {"title": "The Name of the Wind", "author": "Patrick Rothfuss", "isbn": "978-0756404741", "publication_year": 2007, "quantity": 3, "description": "First book in a fantasy series about a gifted young man."},
    {"title": "Norwegian Wood", "author": "Haruki Murakami", "isbn": "978-0375704024", "publication_year": 1987, "quantity": 2, "description": "A coming-of-age novel set in Tokyo."},
    {"title": "The Subtle Art of Not Giving a F*ck", "author": "Mark Manson", "isbn": "978-0062457714", "publication_year": 2016, "quantity": 6, "description": "A counterintuitive approach to living a good life."},
    {"title": "A Brief History of Time", "author": "Stephen Hawking", "isbn": "978-0553380163", "publication_year": 1988, "quantity": 3, "description": "An accessible introduction to cosmology."},
    {"title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "isbn": "978-0486415871", "publication_year": 1866, "quantity": 2, "description": "A psychological novel exploring guilt and redemption."},
    {"title": "The Handmaid's Tale", "author": "Margaret Atwood", "isbn": "978-0385490818", "publication_year": 1985, "quantity": 4, "description": "Dystopian novel about a totalitarian society that treats women as property."},
    {"title": "The Immortal Life of Henrietta Lacks", "author": "Rebecca Skloot", "isbn": "978-1400052189", "publication_year": 2010, "quantity": 3, "description": "Story of Henrietta Lacks and the immortal cell line, HeLa."},
    {"title": "Thinking, Fast and Slow", "author": "Daniel Kahneman", "isbn": "978-0374533557", "publication_year": 2011, "quantity": 4, "description": "Exploration of the two systems that drive the way we think."},
    {"title": "The Kite Runner", "author": "Khaled Hosseini", "isbn": "978-1594631931", "publication_year": 2003, "quantity": 3, "description": "A story of friendship and redemption set in Afghanistan."},
    {"title": "Murder on the Orient Express", "author": "Agatha Christie", "isbn": "978-0062693662", "publication_year": 1934, "quantity": 5, "description": "A classic Hercule Poirot mystery."},
    {"title": "The Power of Habit", "author": "Charles Duhigg", "isbn": "978-0812981605", "publication_year": 2012, "quantity": 4, "description": "An exploration into the science of habit formation."},
    {"title": "The Wind-Up Bird Chronicle", "author": "Haruki Murakami", "isbn": "978-0679775430", "publication_year": 1994, "quantity": 2, "description": "A surreal novel blending personal history and mystery."}
]


def add_books():
    added = 0
    with app.app_context():
        for b in books_to_add:
            existing = Book.query.filter_by(isbn=b['isbn']).first()
            if existing:
                print(f"Skipping existing book: {b['title']} ({b['isbn']})")
                continue
            book = Book(
                title=b['title'],
                author=b['author'],
                isbn=b['isbn'],
                publication_year=b['publication_year'],
                quantity=b.get('quantity', 1),
                available=True,
                description=b.get('description', '')
            )
            db.session.add(book)
            added += 1
        if added:
            db.session.commit()
        print(f"Done. {added} new book(s) added.")


if __name__ == '__main__':
    add_books()
