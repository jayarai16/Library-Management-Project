import sqlite3
import os
p = os.path.join(os.path.dirname(__file__), 'library.db')
conn = sqlite3.connect(p)
cur = conn.cursor()
cur.execute("SELECT name, type FROM sqlite_master WHERE type IN ('table','view')")
rows = cur.fetchall()
print('Tables/views in', p)
for r in rows:
    print(r)
conn.close()
