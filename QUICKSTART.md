# 🚀 QUICK START GUIDE

## 📌 Prerequisites
- Python 3.7+ installed
- pip (comes with Python)

## ⚡ Quick Installation (5 minutes)

### Step 1: Open Terminal/Command Prompt
Navigate to the project folder:
```bash
cd c:\Users\hp\Desktop\lib\library-management-system
```

### Step 2: Create Virtual Environment (Recommended)
**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database with Sample Data
```bash
python init_db.py
```

### Step 5: Run the Application
```bash
python app.py
```

You'll see output like:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### Step 6: Open in Browser
Go to: **http://localhost:5000**

---

## 🔑 Test Accounts

Use these credentials to test the system:

### Admin Account
- **Username:** `admin`
- **Password:** `admin123`
- **Access:** Full system + Admin Panel

### Regular User 1
- **Username:** `john_doe`
- **Password:** `password123`
- **Access:** Regular user features

### Regular User 2
- **Username:** `jane_smith`
- **Password:** `password123`
- **Access:** Regular user features

---

## 📋 Features to Test

### 1. User Authentication
- ✅ Login with existing credentials
- ✅ Register new account
- ✅ Logout functionality

### 2. Browse Books
- ✅ View all books
- ✅ Search by title/author/ISBN
- ✅ Filter by availability

### 3. Borrow Books
- ✅ Click "Borrow Book" on any available book
- ✅ View borrowed books on dashboard
- ✅ Check due dates (14 days from borrow date)

### 4. Return Books
- ✅ Click "Return" button on borrowed book
- ✅ Book becomes available again
- ✅ Borrowing record updated

### 5. Admin Panel (Admin Users Only)
- ✅ Add new books to library
- ✅ View complete inventory
- ✅ Track book availability

---

## 🎯 Project Features Walkthrough

### Dashboard
- Statistics showing borrowed books count
- List of currently borrowed books with due dates
- Recently added books with quick borrow options
- Overdue books highlighted in red

### Browse Books
- Search by title, author, or ISBN
- Filter: All Books / Available / Unavailable
- Book details card view
- Instant borrow functionality

### Admin Panel
- Form to add new books with complete information
- Inventory table showing all books
- Quantity and availability tracking

---

## 🛠️ Folder Structure Explanation

```
library-management-system/
├── app.py                    # Main Flask application (routes & config)
├── models.py                 # Database models (User, Book, Borrowing)
├── config.py                 # Configuration settings
├── init_db.py               # Database initialization with sample data
├── requirements.txt         # Python packages needed
│
├── templates/               # HTML pages
│   ├── base.html           # Navigation and base layout
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── dashboard.html      # User dashboard
│   ├── books.html          # Browse books
│   ├── admin_books.html    # Admin panel
│   └── 404.html, 500.html  # Error pages
│
└── static/                 # CSS, JavaScript, images
    ├── css/style.css       # All styling
    └── js/script.js        # Frontend interactions
```

---

## 🔧 Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:** Make sure you activated the virtual environment and ran `pip install -r requirements.txt`

### Issue: "Port 5000 already in use"
**Solution:** Change port in app.py:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use 5001 instead
```

### Issue: CSS/Images not loading
**Solution:** Clear browser cache (Ctrl+Shift+Delete) and refresh page

### Issue: Database error
**Solution:** Delete `library.db` file and run `python init_db.py` again

---

## 📱 Responsive Design

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones (all major browsers)

---

## 🔐 Security Notes

⚠️ **Important for Production:**
1. Change `SECRET_KEY` in app.py
2. Set `DEBUG = False`
3. Use HTTPS
4. Use strong database passwords
5. Implement CSRF protection
6. Validate all user inputs

---

## 📊 Database Details

**SQLite Database:** `library.db` (auto-created)

**Tables:**
- `users` - User accounts with hashed passwords
- `books` - Book catalog
- `borrowings` - Borrow/Return history

---

## 🚀 Next Steps

1. **Customize:** Edit CSS in `static/css/style.css`
2. **Add Books:** Use Admin Panel or manually add via `init_db.py`
3. **Deploy:** Follow deployment instructions in README.md
4. **Extend:** Add features like email notifications, ratings, etc.

---

## 📞 Support

For issues:
1. Check the troubleshooting section in README.md
2. Verify all files are in correct directories
3. Ensure Python version is 3.7+
4. Check that all dependencies are installed

---

## ✨ Enjoy Using the Library Management System!

**Need help?** Refer to the comprehensive README.md file for detailed documentation.
