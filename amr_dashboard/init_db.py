import sqlite3
from pathlib import Path

def main():
    db_path = Path(__file__).parent / "amr.db"
    conn = sqlite3.connect(db_path)
    with open(Path(__file__).parent / "schema_sqlite.sql") as f:
        conn.executescript(f.read())
    conn.close()
    print("✅ Database initialized and amr.db created successfully.")

if __name__ == "__main__":
    main()