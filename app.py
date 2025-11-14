from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import uuid

# -------------------- App & Config --------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///library.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
from extensions import db
db.init_app(app)

# Import models after `db` is available (models import `db` from extensions)
from models import User, Book, Borrowing, Wishlist, Review

# Ensure tables exist
with app.app_context():
    db.create_all()

# -------------------- Template context --------------------
@app.context_processor
def inject_user():
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return dict(current_user=user)

# -------------------- Routes --------------------
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return redirect(url_for('register'))
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('register'))
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return redirect(url_for('register'))

        hashed = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Account created. Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating account: ' + str(e), 'error')
            return redirect(url_for('register'))

    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if not username or not password:
            flash('Username and password required.', 'error')
            return redirect(url_for('login'))
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'error')
        return redirect(url_for('login'))
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        flash('User not found.', 'error')
        return redirect(url_for('login'))
    borrowed_books = Borrowing.query.filter_by(user_id=user.id, return_date=None).all()
    available_books = Book.query.filter(Book.quantity > 0).all()
    return render_template('dashboard.html', user=user, borrowed_books=borrowed_books, available_books=available_books)

# Browse books
@app.route('/books')
def books():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))
    search = request.args.get('search', '').strip()
    filter_type = request.args.get('filter', 'all')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    query = Book.query
    if search:
        term = f"%{search}%"
        query = query.filter((Book.title.ilike(term)) | (Book.author.ilike(term)) | (Book.isbn.ilike(term)))
    if filter_type == 'available':
        query = query.filter(Book.available == True)
    elif filter_type == 'unavailable':
        query = query.filter(Book.available == False)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    books_list = pagination.items
    total_pages = pagination.pages
    
    return render_template('books.html', books=books_list, search=search, filter_type=filter_type, 
                         page=page, total_pages=total_pages)

# Borrow book
@app.route('/borrow/<int:book_id>', methods=['POST'])
def borrow_book(book_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    book = Book.query.get(book_id)
    if not book:
        flash('Book not found.', 'error')
        return redirect(url_for('books'))
    if book.get_available_count() <= 0:
        flash('No copies available.', 'error')
        return redirect(url_for('books'))
    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=14)
    borrowing = Borrowing(user_id=user.id, book_id=book.id, borrow_date=borrow_date, due_date=due_date)
    # reduce availability logic
    try:
        db.session.add(borrowing)
        db.session.commit()
        flash(f'Borrowed "{book.title}". Due: {due_date.date()}', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error borrowing book: ' + str(e), 'error')
    return redirect(url_for('books'))

# Return book
@app.route('/return/<int:borrowing_id>', methods=['POST'])
def return_book(borrowing_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))
    borrowing = Borrowing.query.get(borrowing_id)
    if not borrowing:
        flash('Record not found.', 'error')
        return redirect(url_for('dashboard'))
    if borrowing.user_id != session['user_id']:
        flash('You can only return your own books.', 'error')
        return redirect(url_for('dashboard'))
    borrowing.return_date = datetime.now()
    try:
        db.session.commit()
        flash('Book returned successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error returning book: ' + str(e), 'error')
    return redirect(url_for('dashboard'))

# Wishlist - Add to wishlist
@app.route('/wishlist/add/<int:book_id>', methods=['POST'])
def add_to_wishlist(book_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    book = Book.query.get(book_id)
    if not book:
        flash('Book not found.', 'error')
        return redirect(url_for('books'))
    
    existing = Wishlist.query.filter_by(user_id=user.id, book_id=book_id).first()
    if existing:
        flash('Book already in wishlist.', 'info')
    else:
        wishlist_item = Wishlist(user_id=user.id, book_id=book_id)
        try:
            db.session.add(wishlist_item)
            db.session.commit()
            flash(f'"{book.title}" added to wishlist.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error adding to wishlist: ' + str(e), 'error')
    return redirect(url_for('books'))

# Wishlist - Remove from wishlist
@app.route('/wishlist/remove/<int:wishlist_id>', methods=['POST'])
def remove_from_wishlist(wishlist_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))
    wishlist_item = Wishlist.query.get(wishlist_id)
    if not wishlist_item or wishlist_item.user_id != session['user_id']:
        flash('Wishlist item not found.', 'error')
        return redirect(url_for('wishlist'))
    try:
        db.session.delete(wishlist_item)
        db.session.commit()
        flash('Removed from wishlist.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error: ' + str(e), 'error')
    return redirect(url_for('wishlist'))

# Wishlist - View wishlist
@app.route('/wishlist')
def wishlist():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    wishlist_items = Wishlist.query.filter_by(user_id=user.id).all()
    return render_template('wishlist.html', wishlist_items=wishlist_items)

# Reviews - Submit review
@app.route('/review/<int:book_id>', methods=['POST'])
def submit_review(book_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    book = Book.query.get(book_id)
    if not book:
        flash('Book not found.', 'error')
        return redirect(url_for('books'))
    
    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment', '').strip()
    
    if not rating or rating < 1 or rating > 5:
        flash('Rating must be between 1 and 5.', 'error')
        return redirect(url_for('book_detail', book_id=book_id))
    
    existing_review = Review.query.filter_by(user_id=user.id, book_id=book_id).first()
    if existing_review:
        existing_review.rating = rating
        existing_review.comment = comment
        existing_review.updated_at = datetime.now()
        action = 'updated'
    else:
        review = Review(user_id=user.id, book_id=book_id, rating=rating, comment=comment)
        db.session.add(review)
        action = 'added'
    
    try:
        db.session.commit()
        flash(f'Review {action} successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error submitting review: ' + str(e), 'error')
    return redirect(url_for('book_detail', book_id=book_id))

# Book detail page
@app.route('/book/<int:book_id>')
def book_detail(book_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))
    book = Book.query.get_or_404(book_id)
    user = User.query.get(session['user_id'])
    reviews = Review.query.filter_by(book_id=book_id).all()
    user_review = Review.query.filter_by(user_id=user.id, book_id=book_id).first()
    wishlist_item = Wishlist.query.filter_by(user_id=user.id, book_id=book_id).first()
    avg_rating = Review.get_average_rating(book_id)
    return render_template('book_detail.html', book=book, reviews=reviews, user_review=user_review, 
                         wishlist_item=wishlist_item, avg_rating=avg_rating)

# Admin - manage books
@app.route('/admin/books', methods=['GET', 'POST'])
def admin_books():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    if not user or not user.is_admin:
        flash('Admin access required.', 'error')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        isbn = request.form.get('isbn', '').strip()
        publication_year = request.form.get('publication_year', '').strip()
        quantity = int(request.form.get('quantity', '1'))
        description = request.form.get('description', '').strip()
        image_url = request.form.get('image_url', '').strip()
        
        # Handle file upload
        if 'cover_file' in request.files:
            file = request.files['cover_file']
            if file and file.filename:
                upload_folder = os.path.join('static', 'uploads', 'covers')
                os.makedirs(upload_folder, exist_ok=True)
                # Generate unique filename
                filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
                file.save(os.path.join(upload_folder, filename))
                image_url = f"/static/uploads/covers/{filename}"
        
        if not title or not author or not isbn or not publication_year:
            flash('All fields required.', 'error')
            return redirect(url_for('admin_books'))
        book = Book(title=title, author=author, isbn=isbn, publication_year=int(publication_year), 
                   quantity=quantity, available=True, description=description, image_url=image_url)
        try:
            db.session.add(book)
            db.session.commit()
            flash('Book added.', 'success')
            return redirect(url_for('admin_books'))
        except Exception as e:
            db.session.rollback()
            flash('Error adding book: ' + str(e), 'error')
    books_list = Book.query.all()
    return render_template('admin_books.html', books=books_list)

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

# -------------------- Run --------------------
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
