import sys
from pathlib import Path
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text, inspect
import amr_dashboard.visualizations as viz
from st_aggrid import AgGrid, GridOptionsBuilder
from fpdf import FPDF

# ----------------------------
# UTILITY FUNCTIONS
# ----------------------------
def clear_pheno_filters():
    st.session_state["pheno_org"] = ""
    st.session_state["pheno_ab"] = ""
    st.session_state["pheno_region"] = ""
    st.session_state["pheno_res"] = "All"

def clear_geno_filters():
    st.session_state["geno_org"] = ""
    st.session_state["geno_mech"] = ""
    st.session_state["geno_gene"] = ""

def df_to_pdf(df, filename="export.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    for col in df.columns:
        pdf.cell(40, 10, col, 1)
    pdf.ln()
    for _, row in df.iterrows():
        for item in row:
            pdf.cell(40, 10, str(item), 1)
        pdf.ln()
    pdf.output(filename)
    return filename

def download_buttons(df, prefix="results", key_csv=None, key_pdf=None):
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, file_name=f"{prefix}.csv", key=key_csv)
    pdf_file = df_to_pdf(df, filename=f"{prefix}.pdf")
    with open(pdf_file, "rb") as f:
        st.download_button("Download PDF", f, file_name=f"{prefix}.pdf", key=key_pdf)

# ----------------------------
# QUERY FUNCTIONS
# ----------------------------
def query_phenotype(engine, organism, antibiotic, region, selected_resistance):
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
        return pd.read_sql(text(query), conn, params=params)

def query_genotype(engine, organism, mechanism, gene):
    query = """
        SELECT 
            Organism,
            gene,
            drug_class,
            Antibiotic,
            mechanism
        FROM card_genes
        WHERE 1=1
    """
    params = {}
    if organism:
        query += " AND Organism = :organism"
        params["organism"] = organism
    if mechanism:
        query += " AND mechanism = :mechanism"
        params["mechanism"] = mechanism
    if gene:
        query += " AND Gene = :gene"
        params["gene"] = gene
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn, params=params)

# ----------------------------
# TAB FUNCTIONS
# ----------------------------
def phenotype_tab(engine):
    st.header("Phenotypic Resistance Profiles")
    organism = st.text_input("Organism", key="pheno_org")
    antibiotic = st.text_input("Antibiotic", key="pheno_ab")
    region = st.text_input("Region", key="pheno_region")
    resistance_levels = ["All", "susceptible", "intermediate", "resistant"]
    selected_resistance = st.radio("Resistance Level", resistance_levels, horizontal=True, key="pheno_res")
    st.button("Clear Filters", on_click=clear_pheno_filters, key="clear_pheno_btn")

    df = query_phenotype(engine, organism, antibiotic, region, selected_resistance)

    st.subheader("Query Results")
    st.dataframe(df, use_container_width=True)

    if not df.empty:
        download_buttons(df, prefix="phenotype_results", key_csv="dl_pheno_csv", key_pdf="dl_pheno_pdf")

        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_selection(selection_mode="single", use_checkbox=False)
        grid_options = gb.build()
        grid_response = AgGrid(df, gridOptions=grid_options, update_mode="MODEL_CHANGED")
        selected = grid_response['selected_rows']
        if selected:
            desc = selected[0].get('Description')
            if desc:
                st.info(desc)

        viz.resistance_level_chart(df)
        viz.trend_chart(df)
        viz.geography_summary(df)
        viz.antibiotic_frequency(df)
        viz.organism_frequency(df)
    else:
        st.info("No results found.")

def genotype_tab(engine):
    st.header("Genotype-Based Resistance (CARD)")
    organism = st.text_input("Organism", key="geno_org")
    mechanism = st.text_input("Mechanism", key="geno_mech")
    gene = st.text_input("Gene", key="geno_gene")
    st.button("Clear Filters", on_click=clear_geno_filters, key="clear_geno_btn")

    df = query_genotype(engine, organism, mechanism, gene)

    st.subheader("Query Results")
    st.dataframe(df, use_container_width=True)

    if not df.empty:
        download_buttons(df, prefix="genotype_results", key_csv="dl_geno_csv", key_pdf="dl_geno_pdf")

        st.subheader("Explore Unique Values")
        col = st.selectbox("Select a column to view unique values:", df.columns, key="unique_col_select")
        unique_vals = df[col].dropna().unique().tolist()
        st.write(unique_vals)

        viz.card_mechanism_summary(df)
        viz.card_drugclass_distribution(df)
        viz.card_gene_frequency(df)
    else:
        st.info("No CARD gene results found.")

# ----------------------------
# MAIN
# ----------------------------
# ----------------------------
# MAIN
# ----------------------------
def main():
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    engine = create_engine("sqlite:///amr_dashboard/amr.db")
    st.title("AMR Resistance Dashboard")

    # Initialize session state defaults
    defaults = {
        "pheno_org": "",
        "pheno_ab": "",
        "pheno_region": "",
        "pheno_res": "All",
        "geno_org": "",
        "geno_mech": "",
        "geno_gene": "",
    }
    for key, val in defaults.items():
        st.session_state.setdefault(key, val)

    # Create tabs
    tab1, tab2 = st.tabs(["Phenotype (Resistance Profiles)", "Genotype (CARD)"])

    # ----------------------------
    # Phenotype Tab
    # ----------------------------
    with tab1:
        st.header("Phenotypic Resistance Profiles")

        pheno_org = st.text_input("Organism (Phenotype)", key="pheno_org")
        pheno_ab = st.text_input("Antibiotic (Phenotype)", key="pheno_ab")
        pheno_region = st.text_input("Region (Phenotype)", key="pheno_region")
        resistance_levels = ["All", "susceptible", "intermediate", "resistant"]
        pheno_res = st.radio("Resistance Level", resistance_levels, horizontal=True, key="pheno_res")

        st.button("Clear Phenotype Filters", on_click=clear_pheno_filters, key="clear_pheno_btn")

        df_pheno = query_phenotype(engine, pheno_org, pheno_ab, pheno_region, pheno_res)
        st.subheader("Query Results")
        st.dataframe(df_pheno, use_container_width=True)

        if not df_pheno.empty:
            download_buttons(df_pheno, prefix="phenotype_results", key_csv="dl_pheno_csv", key_pdf="dl_pheno_pdf")

            gb = GridOptionsBuilder.from_dataframe(df_pheno)
            gb.configure_selection(selection_mode="single", use_checkbox=False)
            grid_options = gb.build()
            grid_response = AgGrid(df_pheno, gridOptions=grid_options, update_mode="MODEL_CHANGED")
            selected = grid_response['selected_rows']
            if selected:
                desc = selected[0].get('Description')
                if desc:
                    st.info(desc)

            viz.resistance_level_chart(df_pheno)
            viz.trend_chart(df_pheno)
            viz.geography_summary(df_pheno)
            viz.antibiotic_frequency(df_pheno)
            viz.organism_frequency(df_pheno)
        else:
            st.info("No results found.")

    # ----------------------------
    # Genotype Tab
    # ----------------------------
    with tab2:
        st.header("Genotype-Based Resistance (CARD)")

        geno_org = st.text_input("Organism (Genotype)", key="geno_org")
        geno_mech = st.text_input("Mechanism (Genotype)", key="geno_mech")
        geno_gene = st.text_input("Gene (Genotype)", key="geno_gene")

        st.button("Clear Genotype Filters", on_click=clear_geno_filters, key="clear_geno_btn")

        df_geno = query_genotype(engine, geno_org, geno_mech, geno_gene)
        st.subheader("Query Results")
        st.dataframe(df_geno, use_container_width=True)

        if not df_geno.empty:
            download_buttons(df_geno, prefix="genotype_results", key_csv="dl_geno_csv", key_pdf="dl_geno_pdf")

            st.subheader("Explore Unique Values")
            col = st.selectbox("Select a column to view unique values:", df_geno.columns, key="unique_col_select")
            unique_vals = df_geno[col].dropna().unique().tolist()
            st.write(unique_vals)

            viz.card_mechanism_summary(df_geno)
            viz.card_drugclass_distribution(df_geno)
            viz.card_gene_frequency(df_geno)
        else:
            st.info("No CARD gene results found.")


if __name__ == "__main__":
    main()
