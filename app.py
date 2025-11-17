import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///amr.db")

st.title("AMR Resistance Dashboard")

# Filters
organism = st.text_input("Organism")
antibiotic = st.text_input("Antibiotic")
region = st.text_input("Region")

# Query
query = """
SELECT o.name as Organism, a.name as Antibiotic, r.Region, r.Year, r.Resistance_Level, r.MIC_Value
FROM resistance_profiles r
JOIN Organisms o ON r.organism_id = o.organism_id
JOIN Antibiotics a ON r.antibiotic_id = a.antibiotic_id
WHERE 1=1
"""
params = {}

if organism:
    query += " AND o.name = :organism"
    params["organism"] = organism
if antibiotic:
    query += " AND a.name = :antibiotic"
    params["antibiotic"] = antibiotic
if region:
    query += " AND r.region = :region"
    params["region"] = region

with engine.connect() as conn:
    df = pd.read_sql(text(query), conn, params=params)

st.write(df)

# Simple visualization
if not df.empty:
    st.bar_chart(df['Resistance_Level'].value_counts())
