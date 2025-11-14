import sqlite3
import shutil
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'library.db')
BACKUP_DIR = os.path.join(BASE_DIR, 'backups')

os.makedirs(BACKUP_DIR, exist_ok=True)

timestamp = time.strftime('%Y%m%d_%H%M%S')
backup_path = os.path.join(BACKUP_DIR, f'instance_library.db.bak.{timestamp}')

if os.path.exists(DB_PATH):
    shutil.copy2(DB_PATH, backup_path)
    print(f'Backup created at: {backup_path}')
else:
    print('Instance database file not found; nothing to backup.')

# Connect and check
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Check if column exists
cur.execute("PRAGMA table_info(books)")
cols = [row[1] for row in cur.fetchall()]
print('Current columns in books table:', cols)

if 'image_url' in cols:
    print('Column image_url already exists in instance DB. No change needed.')
else:
    try:
        cur.execute("ALTER TABLE books ADD COLUMN image_url TEXT;")
        conn.commit()
        print('Added column image_url to books table in instance DB.')
    except Exception as e:
        print('Error adding column:', e)

# Print final schema info
cur.execute("PRAGMA table_info(books)")
for row in cur.fetchall():
    print(row)

conn.close()
print('Done.')
