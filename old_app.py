import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import visualizations as viz
from st_aggrid import AgGrid, GridOptionsBuilder


engine = create_engine("sqlite:///amr.db")

st.title("AMR Resistance Dashboard")

#  TAB LAYOUT
tab1, tab2 = st.tabs(["Phenotype (Resistance Profiles)", "Genotype (CARD)"])

#  TAB 1 — PHENOTYPE DASHBOARD
with tab1:
    st.header("Phenotypic Resistance Profiles")

    organism = st.text_input("Organism", key="pheno_org")
    antibiotic = st.text_input("Antibiotic", key="pheno_ab")
    region = st.text_input("Region", key="pheno_region")

    # Radio buttons for resistance levels
    resistance_levels = ["All", "Susceptible", "Intermediate", "Resistant"]
    selected_resistance = st.radio("Resistance Level", resistance_levels, horizontal=True)


    query = """
    SELECT scientific_name AS Organism,
           antibiotic AS Antibiotic,
           location AS Region,
           resistance_phenotype AS Resistance_Level,
           mic_mg_L AS MIC_Value,
           create_date AS Year,
           notes AS Description
    FROM resistance_profiles
    WHERE 1=1
    """

    params = {}

    if organism:
        query += " AND scientific_name = :organism"
        params["organism"] = organism
    if antibiotic:
        query += " AND antibiotic = :antibiotic"
        params["antibiotic"] = antibiotic
    if region:
        query += " AND location = :region"
        params["region"] = region
    if selected_resistance != "All":
        query += " AND resistance_phenotype = :res_level"
        params["res_level"] = selected_resistance.lower()

    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn, params=params)

    st.subheader("Query Results")
    st.dataframe(df, use_container_width=True)

    if df.empty:
        st.info("No results found.")
    else:
        # Easy way to select unique values
        st.subheader("Explore Unique Values")

        col = st.selectbox("Select a column to view unique values:", df.columns)

        unique_vals = df[col].dropna().unique().tolist()
        st.write(unique_vals)
        
        viz.resistance_level_chart(df)
        viz.trend_chart(df)
        viz.geography_summary(df)
        viz.antibiotic_frequency(df)
        viz.organism_frequency(df)

#  TAB 2 — GENOTYPE DASHBOARD (CARD DATA)
with tab2:
    st.header("Genotype-Based Resistance (CARD)")

    organism2 = st.text_input("Organism", key="geno_org")
    mechanism2 = st.text_input("Mechanism", key="geno_mech")
    gene2 = st.text_input("Gene", key="geno_gene")

    query2 = """
    SELECT 
        Organism,
        gene,
        drug_class,
        Antibiotic,
        mechanism
    FROM card_genes
    WHERE 1=1
    """

    params2 = {}

    if organism2:
        query2 += " AND Organism = :organism"
        params2["organism"] = organism2

    if mechanism2:
        query2 += " AND mechanism = :mechanism"
        params2["mechanism"] = mechanism2

    if gene2:
        query2 += " AND Gene = :gene"
        params2["gene"] = gene2

    with engine.connect() as conn:
        df2 = pd.read_sql(text(query2), conn, params=params2)

    st.subheader("Query Results")
    st.dataframe(df2, use_container_width=True)

    if df2.empty:
        st.info("No CARD gene results found.")
    else:
        # Easy way to select unique values
        st.subheader("Explore Unique Values")

        col = st.selectbox("Select a column to view unique values:", df2.columns)

        unique_vals = df2[col].dropna().unique().tolist()
        st.write(unique_vals)
        
        viz.card_mechanism_summary(df2)
        viz.card_drugclass_distribution(df2)
        viz.card_gene_frequency(df2)