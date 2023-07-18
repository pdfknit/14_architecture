import sqlite3

from framework.config import DATABASE_NAME

con = sqlite3.connect(DATABASE_NAME)
cur = con.cursor()
with open('create_db.sql', 'r') as f:
    text = f.read()
cur.executescript(text)
cur.close()
con.close()
