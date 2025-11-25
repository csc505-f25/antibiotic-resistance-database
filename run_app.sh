#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Navigate to project root (optional, adjust if needed)
cd "$(dirname "$0")"

# Path to requirements file
REQ_FILE="documentation/requirements.txt"

# Upgrade pip first
python3 -m pip install --upgrade pip

# Install dependencies
if [ -f "$REQ_FILE" ]; then
    echo "Installing dependencies from $REQ_FILE..."
    python3 -m pip install -r "$REQ_FILE"
else
    echo "Requirements file not found at $REQ_FILE"
    exit 1
fi

# Initialize database if missing
cd amr_dashboard
DB_FILE="amr_dashboard/amr.db"
if [ ! -f "$DB_FILE" ]; then
    echo "Database not found. Initializing..."
    python3 init_db.py
    python3 load_data.py
else
    echo "Database already exists. Skipping initialization."
fi

# Run the Streamlit app
echo "Launching Streamlit app..."
streamlit run app.py
