# This file lives at the repo root so Streamlit Cloud can run it.
# It simply imports and runs the actual app.

import os
from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).parent / "amr_dashboard" / "amr.db"

# Auto-create DB on Streamlit Cloud if missing
if not DB_PATH.exists():
    import subprocess
    import amr_dashboard.init_db as initdb

    print("Creating fresh amr.db on Streamlit Cloud...")
    initdb.main()  # make sure init_db.py has a main() that builds the DB

from amr_dashboard.app import main

if __name__ == "__main__":
    main()
