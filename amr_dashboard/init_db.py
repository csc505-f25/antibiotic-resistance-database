import sqlite3
from pathlib import Path

def main():
    DB_PATH = Path(__file__).parent / "amr.db"
    SCHEMA_PATH = Path(__file__).parent / "schema_sqlite.sql"

    if DB_PATH.exists():
        print("Database already exists. Skipping creation.")
        return

    with sqlite3.connect(DB_PATH) as conn:
        with open(SCHEMA_PATH, "r") as f:
            conn.executescript(f.read())
    print(f"✅ Database created at {DB_PATH}")
