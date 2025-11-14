# 📚 Library Management System

A comprehensive web-based library management system built with Python (Flask), SQLite, HTML, and CSS. This system allows users to create accounts, log in, browse books, borrow and return books, and provides admin functionality for managing the library inventory.

## ✨ Features

### User Features
- **User Authentication**
  - Register new account with validation
  - Secure login with password hashing
  - Logout functionality
  - Session management

- **Book Management**
  - Browse complete library catalog
  - Search books by title, author, or ISBN
  - Filter books by availability status
  - View detailed book information

- **Borrowing System**
  - Borrow available books
  - 14-day borrowing period
  - Track borrowed books in dashboard
  - Return books with automatic availability update
  - Overdue tracking with visual indicators
  - Days until due calculation

- **Dashboard**
  - View personal profile
  - See currently borrowed books
  - Check due dates and overdue status
  - Quick access to recently added books
  - Statistics (borrowed books, available books, borrow period)

### Admin Features
- **Book Inventory Management**
  - Add new books to library
  - Track book quantities
  - Monitor availability status
  - View complete inventory list
  - Admin-only access panel

## 🏗️ Project Structure

```
library-management-system/
│
├── app.py                          # Main Flask application
├── models.py                       # Database models (User, Book, Borrowing)
├── requirements.txt                # Python dependencies
├── library.db                      # SQLite database (auto-created)
│
├── templates/                      # HTML templates
│   ├── base.html                  # Base template with navigation
│   ├── login.html                 # Login page
│   ├── register.html              # User registration page
│   ├── dashboard.html             # User dashboard
│   ├── books.html                 # Book browsing page
│   ├── admin_books.html           # Admin panel for book management
│   ├── 404.html                   # 404 error page
│   └── 500.html                   # 500 error page
│
├── static/                        # Static files
│   ├── css/
│   │   └── style.css             # Complete styling with responsive design
│   └── js/
│       └── script.js             # Frontend JavaScript utilities
│
└── README.md                      # This file
```

## 🗄️ Database Schema

### Users Table
- `id` (Integer, Primary Key)
- `username` (String, Unique)
- `email` (String, Unique)
- `password` (String, Hashed)
- `is_admin` (Boolean)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Books Table
- `id` (Integer, Primary Key)
- `title` (String)
- `author` (String)
- `isbn` (String, Unique)
- `publication_year` (Integer)
- `quantity` (Integer)
- `available` (Boolean)
- `description` (Text)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Borrowings Table
- `id` (Integer, Primary Key)
- `user_id` (Integer, Foreign Key)
- `book_id` (Integer, Foreign Key)
- `borrow_date` (DateTime)
- `due_date` (DateTime)
- `return_date` (DateTime, Nullable)

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone/Download Project
```bash
# Navigate to the project directory
cd library-management-system
```

### Step 2: Create Virtual Environment (Optional but Recommended)
```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database
```bash
# The database will be created automatically when you run the app
# But you can initialize it manually by running:
python -c "from app import db; db.create_all()"
```

### Step 5: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

## 📖 Usage Guide

### First Time Setup

1. **Create Admin Account**
   - Register a new account
   - Once registered, manually set `is_admin = True` in the database or modify the registration logic

2. **Add Books (Admin)**
   - Go to Admin Panel (accessible if your account has `is_admin = True`)
   - Add books with details: Title, Author, ISBN, Publication Year, Quantity
   - Books become immediately available for borrowing

### Regular User Flow

1. **Register Account**
   - Click "Create Account"
   - Enter username, email, and password
   - Click "Create Account"

2. **Login**
   - Enter username and password
   - Click "Login"
   - You'll be directed to your dashboard

3. **Browse Books**
   - Click "Browse Books" in navigation
   - Search by title, author, or ISBN
   - Filter by availability status
   - Click "Borrow Book" to borrow

4. **Manage Borrowed Books**
   - View borrowed books on Dashboard
   - See due dates and days remaining
   - Return books when finished
   - Check for overdue indicators (red badges)

5. **Logout**
   - Click the "Logout" button in the top right
   - You'll be logged out and redirected to login page

## 🔐 Security Features

- **Password Hashing**: Passwords are hashed using Werkzeug security
- **Session Management**: Secure session-based authentication
- **CSRF Protection**: (Can be added with Flask-WTF)
- **Input Validation**: All user inputs are validated
- **SQL Injection Prevention**: Uses SQLAlchemy ORM

## 🎨 Features Showcase

### Responsive Design
- Mobile-friendly interface
- Adapts to tablets and desktops
- Touch-friendly buttons and forms
- Optimal layout on all screen sizes

### User Interface
- Clean, modern design
- Intuitive navigation
- Clear visual hierarchy
- Consistent color scheme
- Helpful icons and badges

### Alert System
- Success messages (green)
- Error messages (red)
- Info messages (blue)
- Warning messages (yellow)
- Auto-dismissing notifications

## 🛠️ Customization

### Change Secret Key (IMPORTANT for Production)
Edit `app.py`:
```python
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
```

### Change Database Location
Edit `app.py`:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
```

### Adjust Borrowing Period
Edit `app.py` in the `borrow_book()` function:
```python
due_date = borrow_date + timedelta(days=14)  # Change 14 to desired days
```

### Customize Styling
Edit `static/css/style.css` - All colors and layouts can be customized

## 🐛 Troubleshooting

### Issue: Import Error for models
**Solution**: Make sure you're in the project directory and Flask can find the modules.

### Issue: Database locked error
**Solution**: Close any other instances of the app and check for .db-journal files

### Issue: Static files not loading
**Solution**: Ensure the `static` folder structure is correct and run the app from the project root directory

### Issue: CSS not applying
**Solution**: Clear browser cache (Ctrl+Shift+Delete) and reload the page

## 📊 Database Initialization Script

To initialize the database with sample data, create a script:

```python
from app import app, db
from models import User, Book
from werkzeug.security import generate_password_hash

with app.app_context():
    # Create tables
    db.create_all()
    
    # Add sample books
    sample_books = [
        Book(title="The Great Gatsby", author="F. Scott Fitzgerald", 
             isbn="978-0-7432-7356-5", publication_year=1925, quantity=3),
        Book(title="To Kill a Mockingbird", author="Harper Lee", 
             isbn="978-0-06-112008-4", publication_year=1960, quantity=2),
        Book(title="1984", author="George Orwell", 
             isbn="978-0-4525-2612-0", publication_year=1949, quantity=1),
    ]
    
    for book in sample_books:
        db.session.add(book)
    
    db.session.commit()
    print("Database initialized with sample data!")
```

## 🔄 API Routes Reference

### Authentication Routes
- `GET /` - Home (redirects to dashboard if logged in)
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET /logout` - User logout

### User Routes
- `GET /dashboard` - User dashboard
- `GET /books` - Browse books
- `POST /borrow/<book_id>` - Borrow a book
- `POST /return/<borrowing_id>` - Return a book

### Admin Routes
- `GET/POST /admin/books` - Manage books

### Error Routes
- `GET /404` - Page not found
- `GET /500` - Server error

## 📋 Requirements

```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Werkzeug==2.3.7
SQLAlchemy==2.0.20
```

## 🚀 Deployment

### For Production:
1. Change `debug=False` in `app.py`
2. Use a production WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn app:app
   ```
3. Use a proper database (PostgreSQL, MySQL)
4. Set strong SECRET_KEY
5. Enable HTTPS
6. Set up proper error logging

## 📝 Future Enhancements

- [ ] Email notifications for due dates
- [ ] Fine system for overdue books
- [ ] Book reservations
- [ ] Wishlist feature
- [ ] Reading history
- [ ] Book ratings and reviews
- [ ] Advanced search filters
- [ ] PDF export of borrowing history
- [ ] SMS notifications
- [ ] Two-factor authentication
- [ ] Book categories and tags
- [ ] Recommendations engine

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Library Management System v1.0
Created: 2025

## 📞 Support

For issues or questions, please refer to the troubleshooting section or create an issue in the repository.

---

**Happy Reading!** 📚✨
