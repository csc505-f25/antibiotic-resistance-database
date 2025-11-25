import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

DB = "amr.db"

# ---- Database helpers ----
def get_distinct_organisms():
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query("""
        SELECT DISTINCT o.name
        FROM organisms o
        JOIN resistance_profiles rp ON rp.organism_id = o.organism_id
        ORDER BY o.name
    """, conn)
    conn.close()
    return ["(any)"] + df["name"].tolist()

def get_distinct_antibiotics():
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query("""
        SELECT DISTINCT a.name
        FROM antibiotics a
        JOIN resistance_profiles rp ON rp.antibiotic_id = a.antibiotic_id
        ORDER BY a.name
    """, conn)
    conn.close()
    return ["(any)"] + df["name"].tolist()

def get_distinct_regions():
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query("SELECT DISTINCT region FROM resistance_profiles ORDER BY region", conn)
    conn.close()
    return ["(any)"] + df["region"].dropna().tolist()

def query_data(organism=None, antibiotic=None, region=None):
    conn = sqlite3.connect(DB)
    query = """
        SELECT 
            o.name AS organism,
            a.name AS antibiotic,
            d.name AS drug_class,
            rp.resistance_level,
            rp.year,
            rp.region
        FROM resistance_profiles rp
        JOIN organisms o ON rp.organism_id = o.organism_id
        JOIN antibiotics a ON rp.antibiotic_id = a.antibiotic_id
        LEFT JOIN drug_classes d ON a.drug_class_id = d.drug_class_id
        WHERE 1=1
    """

    params = []

    if organism and organism != "(any)":
        query += " AND o.name LIKE ?"
        params.append(f"%{organism}%")

    if antibiotic and antibiotic != "(any)":
        query += " AND a.name LIKE ?"
        params.append(f"%{antibiotic}%")

    if region and region != "(any)":
        query += " AND rp.region LIKE ?"
        params.append(f"%{region}%")

    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


# ---- Streamlit UI ----

st.title("🧬 Antibiotic Resistance Dashboard (Phase 1)")

# Dropdown filters
organism = st.selectbox("Organism", get_distinct_organisms())
antibiotic = st.selectbox("Antibiotic", get_distinct_antibiotics())
region = st.selectbox("Region", get_distinct_regions())

# Run query
df = query_data(organism, antibiotic, region)

st.subheader("Results")
st.dataframe(df)

# ---- Visualization example ----
if not df.empty:
    st.subheader("Resistance Level by Year")
    fig, ax = plt.subplots()
    df.groupby("year")["resistance_level"].count().plot(ax=ax)
    ax.set_xlabel("Year")
    ax.set_ylabel("Count")
    st.pyplot(fig)
else:
    st.info("No results found for current filters.")
