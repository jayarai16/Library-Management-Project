from extensions import db
from datetime import datetime

class User(db.Model):
    """User model for library management system"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    borrowings = db.relationship('Borrowing', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def get_borrowed_books_count(self):
        """Get count of currently borrowed books"""
        return len([b for b in self.borrowings if b.return_date is None])
    
    def get_overdue_books(self):
        """Get list of overdue books"""
        from datetime import datetime as dt
        overdue = []
        for borrowing in self.borrowings:
            if borrowing.return_date is None and borrowing.due_date < dt.now():
                overdue.append(borrowing)
        return overdue


class Book(db.Model):
    """Book model for library management system"""
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    author = db.Column(db.String(120), nullable=False, index=True)
    isbn = db.Column(db.String(13), unique=True, nullable=False, index=True)
    publication_year = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    available = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(512), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    borrowings = db.relationship('Borrowing', backref='book', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Book {self.title}>'
    
    def get_available_count(self):
        """Get count of available copies"""
        borrowed_count = len([b for b in self.borrowings if b.return_date is None])
        return self.quantity - borrowed_count
    
    def is_available(self):
        """Check if at least one copy is available"""
        return self.get_available_count() > 0


class Borrowing(db.Model):
    """Borrowing model to track book checkouts"""
    __tablename__ = 'borrowings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False, index=True)
    borrow_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<Borrowing {self.user_id} - {self.book_id}>'
    
    def is_overdue(self):
        """Check if the borrowing is overdue"""
        from datetime import datetime as dt
        return self.return_date is None and self.due_date < dt.now()
    
    def days_until_due(self):
        """Get days remaining until due"""
        from datetime import datetime as dt
        if self.return_date is None:
            remaining = (self.due_date - dt.now()).days
            return max(remaining, 0)
        return 0
    
    def days_overdue(self):
        """Get days overdue"""
        from datetime import datetime as dt
        if self.return_date is None and self.is_overdue():
            return (dt.now() - self.due_date).days
        return 0


class Wishlist(db.Model):
    """Wishlist model to save books for later"""
    __tablename__ = 'wishlists'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False, index=True)
    added_at = db.Column(db.DateTime, default=datetime.now)
    
    # Relationships
    user = db.relationship('User', backref='wishlist')
    book = db.relationship('Book', backref='wishlisted_by')
    
    __table_args__ = (db.UniqueConstraint('user_id', 'book_id', name='_user_book_uc'),)
    
    def __repr__(self):
        return f'<Wishlist {self.user_id} - {self.book_id}>'


class Review(db.Model):
    """Review model for book ratings and comments"""
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False, index=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    user = db.relationship('User', backref='reviews')
    book = db.relationship('Book', backref='reviews')
    
    __table_args__ = (db.UniqueConstraint('user_id', 'book_id', name='_user_book_review_uc'),)
    
    def __repr__(self):
        return f'<Review {self.user_id} - {self.book_id} ({self.rating}★)>'
    
    @staticmethod
    def get_average_rating(book_id):
        """Get average rating for a book"""
        from sqlalchemy import func
        avg = db.session.query(func.avg(Review.rating)).filter_by(book_id=book_id).scalar()
        return round(avg, 1) if avg else 0
    
    @staticmethod
    def get_review_count(book_id):
        """Get number of reviews for a book"""
        return Review.query.filter_by(book_id=book_id).count()
