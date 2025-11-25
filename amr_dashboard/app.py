import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from st_aggrid import AgGrid, GridOptionsBuilder
import export_utils as export
import visualizations as viz

# Export tools
def export_tool(df, figs, chart_file, table_file):
    st.subheader("Export Charts")

    # Export charts
    if st.button("Generate Chart PDF", key=f"gen_charts_{chart_file}"):
        filename = export.export_chart_pdf(figs, chart_file)
        with open(filename, "rb") as f:
            st.download_button(
                "Download Chart PDF",
                f,
                file_name=chart_file,
                key=f"dl_charts_{chart_file}"
            )

    st.subheader("Export Table")

    # Export table PDF
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate Table PDF", key=f"gen_table_{table_file}"):
            filename = export.df_to_pdf(df, table_file)
            with open(filename, "rb") as f:
                st.download_button(
                    "Download Table PDF",
                    f,
                    file_name=table_file,
                    key=f"dl_table_{table_file}"
                )

    # Export table Excel
    with col2:
        excel_file = table_file.replace(".pdf", ".xlsx")
        if st.button("Generate Excel File", key=f"gen_excel_{excel_file}"):
            filename = export.df_to_excel(df, excel_file)
            with open(filename, "rb") as f:
                st.download_button(
                    "Download Table Excel",
                    f,
                    file_name=excel_file,
                    key=f"dl_excel_{excel_file}"
                )

engine = create_engine("sqlite:///amr.db")
st.set_page_config(page_title="AMR Resistance Dashboard", layout="wide")
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

    query = """
    SELECT scientific_name AS Organism,
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

        pie_colors = ["#0068c9", '#83c9ff', '#FF2B2B', '#ffabab', '#4ebdae', '#7defa1', '#ff8700', '#ffd16a', '#6d3fc0', '#d5dae5', '#309bff', '#e9f5ff', '#ff9191', '#FFFFFF', '#64dbca']

        # Charts
        figs = []
        figs.append(viz.resistance_level_chart(df))
        figs[0].update_traces(marker=dict(colors=pie_colors))
        figs[0].update_layout(paper_bgcolor="white", plot_bgcolor="white")
        figs.append(viz.trend_chart(df))
        figs[1].update_traces(marker=dict(color="#0068c9"))
        figs[1].update_layout(paper_bgcolor="white", plot_bgcolor="white")
        viz.geography_summary(df)
        figs.append(viz.antibiotic_frequency(df))
        figs[2].update_traces(marker=dict(color="#0068c9"))
        figs[2].update_layout(paper_bgcolor="white", plot_bgcolor="white")
        figs.append(viz.organism_frequency(df))
        figs[3].update_traces(marker=dict(color="#0068c9"))
        figs[3].update_layout(paper_bgcolor="white", plot_bgcolor="white")
        export_tool(df, figs, "phenotype_charts.pdf", "phenotype_table.pdf")


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
        
        figs2 = []
        figs2.append(viz.card_mechanism_summary(df2))
        figs2[0].update_traces(marker=dict(colors=pie_colors))
        figs2[0].update_layout(paper_bgcolor="white", plot_bgcolor="white")
        figs2.append(viz.card_drugclass_distribution(df2))
        figs2[1].update_traces(marker=dict(color="#0068c9"))
        figs2[1].update_layout(paper_bgcolor="white", plot_bgcolor="white")
        figs2.append(viz.card_gene_frequency(df2))
        figs2[2].update_traces(marker=dict(color="#0068c9"))
        figs2[2].update_layout(paper_bgcolor="white", plot_bgcolor="white")
        

        export_tool(df2, figs2, "genotype_charts.pdf", "genotype_table.pdf")