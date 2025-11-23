import sqlite3

conn = sqlite3.connect("amr.db")
with open("schema_sqlite.sql") as f:
    conn.executescript(f.read())
conn.close()

print("✅ Database initialized and amr.db created successfully.")
