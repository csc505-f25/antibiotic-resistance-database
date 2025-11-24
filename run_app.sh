#!/bin/bash

# Get directory where this script is located
script_dir="$(dirname "$0")"

# Change to that directory
cd "$script_dir" || exit 1

ls
set -e

# Upgrade pip
python3.10 -m pip install --upgrade pip

# Install required packages
python3.10 -m pip install \
    streamlit \
    pandas \
    sqlalchemy \
    fpdf2 \
    streamlit-aggrid \
    plotly \
    matplotlib \
    --quiet

echo "All required packages installed."

# Run Streamlit app
python3.10 -m streamlit run streamlit_app.py
