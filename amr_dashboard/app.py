import sys
from pathlib import Path
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text, inspect
import amr_dashboard.visualizations as viz
from st_aggrid import AgGrid, GridOptionsBuilder

def main():
    # Add the parent directory (antibiotic-resistance-database/) to Python’s module search path
    sys.path.append(str(Path(__file__).resolve().parent.parent))

    #db_path = Path(__file__).parent / "amr.db"  # points to amr_dashboard/amr.db
    engine = create_engine(f"sqlite:///amr_dashboard/amr.db")

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
        resistance_levels = ["All", "susceptible", "intermediate", "resistant"]
        selected_resistance = st.radio("Resistance Level", resistance_levels, horizontal=True)

        inspector = inspect(engine)
        columns = inspector.get_columns("resistance_profiles")
        for col in columns:
            print(col["name"])
        query = """
        SELECT
            scientific_name AS Organism,
            antibiotic AS Antibiotic,
            location AS Region,
            resistance_phenotype AS Resistance_Level,
            mic_mg_L AS MIC_Value,
            year AS Year
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
            params["res_level"] = selected_resistance
                
        
        with engine.connect() as conn:
            df = pd.read_sql(text(query), conn, params=params)

        st.subheader("Query Results")
        st.dataframe(df, use_container_width=True)

        if df.empty:
            st.info("No results found.")
        else:
            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_selection(selection_mode="single", use_checkbox=False)
            grid_options = gb.build()

            grid_response = AgGrid(
                df,
                gridOptions=grid_options,
                enable_enterprise_modules=False,
                update_mode="MODEL_CHANGED"
            )

            # Show description for clicked row
            selected = grid_response['selected_rows']
            if selected:
                desc = selected[0].get('Description')
                if desc:
                    st.info(desc)

            # Charts
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

if __name__ == "__main__":
    main()