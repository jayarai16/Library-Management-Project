"""
Initialize Database with Sample Data
Run this script to populate the database with sample books and users
"""

from app import app, db
from models import User, Book
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize database with sample data"""
    
    with app.app_context():
        # Drop all tables (for testing only)
        # db.drop_all()
        
        # Create all tables
        db.create_all()
        print("✓ Database tables created successfully!")
        
        # Check if data already exists
        if User.query.first():
            print("⚠ Database already contains data. Skipping initialization.")
            return
        
        # Create sample users
        admin_user = User(
            username='admin',
            email='admin@library.com',
            password=generate_password_hash('admin123'),
            is_admin=True
        )
        
        regular_user = User(
            username='john_doe',
            email='john@example.com',
            password=generate_password_hash('password123'),
            is_admin=False
        )
        
        another_user = User(
            username='jane_smith',
            email='jane@example.com',
            password=generate_password_hash('password123'),
            is_admin=False
        )
        
        db.session.add_all([admin_user, regular_user, another_user])
        print("✓ Sample users created!")
        
        # Create sample books
        sample_books = [
                Book(
                    title="The Great Gatsby",
                    author="F. Scott Fitzgerald",
                    isbn="978-0-7432-7356-5",
                    publication_year=1925,
                    quantity=3,
                    available=True,
                    image_url="https://covers.openlibrary.org/b/isbn/9780743273565-L.jpg",
                    description="A classic American novel set in the Jazz Age, exploring wealth and the American Dream."
                ),
            Book(
                title="To Kill a Mockingbird",
                author="Harper Lee",
                isbn="978-0-06-112008-4",
                publication_year=1960,
                quantity=2,
                available=True,
                description="A gripping tale of racial injustice and childhood innocence in the American South."
            ),
                Book(
                    title="1984",
                    author="George Orwell",
                    isbn="978-0-4525-2612-0",
                    publication_year=1949,
                    quantity=2,
                    available=True,
                    image_url="https://covers.openlibrary.org/b/isbn/9780451524935-L.jpg",
                    description="A dystopian novel exploring totalitarianism, surveillance, and oppression."
                ),
            Book(
                title="Pride and Prejudice",
                author="Jane Austen",
                isbn="978-0-14-143951-8",
                publication_year=1813,
                quantity=3,
                available=True,
                description="A romantic novel set in Georgian England, exploring marriage, class, and social expectations."
            ),
            Book(
                title="The Catcher in the Rye",
                author="J.D. Salinger",
                isbn="978-0-316-76948-0",
                publication_year=1951,
                quantity=2,
                available=True,
                description="A coming-of-age novel following a teenage protagonist navigating adulthood in New York."
            ),
            Book(
                title="Brave New World",
                author="Aldous Huxley",
                isbn="978-0-06-085052-4",
                publication_year=1932,
                quantity=2,
                available=True,
                description="A futuristic novel depicting a seemingly perfect society controlled through conditioning."
            ),
            Book(
                title="Jane Eyre",
                author="Charlotte Brontë",
                isbn="978-0-14-044930-3",
                publication_year=1847,
                quantity=2,
                available=True,
                description="A Gothic romance following the passionate life of an orphaned governess."
            ),
            Book(
                title="The Hobbit",
                author="J.R.R. Tolkien",
                isbn="978-0-547-92822-8",
                publication_year=1937,
                quantity=3,
                available=True,
                description="An adventure fantasy following a hobbit on an unexpected journey through a magical world."
            ),
            Book(
                title="Wuthering Heights",
                author="Emily Brontë",
                isbn="978-0-14-043951-8",
                publication_year=1847,
                quantity=1,
                available=True,
                description="A dark romance set on the Yorkshire moors exploring love, revenge, and redemption."
            ),
            Book(
                title="The Lord of the Rings",
                author="J.R.R. Tolkien",
                isbn="978-0-544-00341-1",
                publication_year=1954,
                quantity=2,
                available=True,
                description="An epic fantasy trilogy following the quest to destroy a powerful ring."
            ),
            Book(
                title="Moby Dick",
                author="Herman Melville",
                isbn="978-0-14-043965-5",
                publication_year=1851,
                quantity=2,
                available=True,
                description="An adventure novel following Captain Ahab's obsessive quest for a white whale."
            ),
            Book(
                title="The Picture of Dorian Gray",
                author="Oscar Wilde",
                isbn="978-0-14-043833-7",
                publication_year=1890,
                quantity=2,
                available=True,
                description="A philosophical horror novel exploring vanity, morality, and corruption."
            ),
        ]
        
        for book in sample_books:
            db.session.add(book)
        
        print(f"✓ {len(sample_books)} sample books created!")
        
        # Commit all changes
        db.session.commit()
        
        print("\n" + "="*50)
        print("✓ DATABASE INITIALIZATION COMPLETE!")
        print("="*50)
        print("\nTest Accounts:")
        print("  Admin Account:")
        print("    Username: admin")
        print("    Password: admin123")
        print("\n  Regular User Account:")
        print("    Username: john_doe")
        print("    Password: password123")
        print("\n  Another User Account:")
        print("    Username: jane_smith")
        print("    Password: password123")
        print("\n" + "="*50 + "\n")

if __name__ == '__main__':
    init_database()
