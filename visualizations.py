import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import plotly.express as px


#  Bar & pie charts for resistane levels
def resistance_level_chart(df: pd.DataFrame):
    st.subheader("Resistance Level Counts")
    
    # Count each resistance category
    counts = df["Resistance_Level"].value_counts().reset_index()
    counts.columns = ["Resistance_Level", "Count"]

    # Bar chart
    st.bar_chart(df["Resistance_Level"].value_counts())
    
    # Pie chart
    fig = px.pie(
        counts,
        names="Resistance_Level",
        values="Count",
        title="Resistance Level Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# Line chart to view resistance trends over time
def trend_chart(df: pd.DataFrame):
    st.subheader("Resistance Trends Over Time")

    # Ensure correct column name
    if "year" in df.columns:
        df_year = df.groupby("year")["Resistance_Level"].count().reset_index()
        df_year = df_year.rename(columns={"year": "Year"})
    else:
        df_year = df.groupby("Year")["Resistance_Level"].count().reset_index()

    df_year = df_year.sort_values("Year")

    # Create Plotly line chart
    fig = px.line(
        df_year,
        x="Year",
        y="Resistance_Level",
        markers=True,
        title="Reports by Year",
    )
    
    # Add scroll + zoom
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(visible=True),  # draggable slider
            rangemode='normal',
        ),
        height=450,
    )

    st.plotly_chart(fig, use_container_width=True)

# Chart of resistance reports organized by region
def geography_summary(df: pd.DataFrame):
    st.subheader("🌍 Reports by Region")
    df_geo = df.groupby("Region")["Resistance_Level"].count().reset_index()
    st.dataframe(df_geo.sort_values("Resistance_Level", ascending=False))

def antibiotic_frequency(df: pd.DataFrame):
    st.subheader("Antibiotic Frequency")

    df_ab = (
        df.groupby("Antibiotic")["Resistance_Level"]
        .count()
        .reset_index()
        .rename(columns={"Resistance_Level": "Count"})
        .sort_values("Count", ascending=False)
    )

    fig = px.bar(
        df_ab,
        x="Count",
        y="Antibiotic",
        orientation="h",  # horizontal bars = easier to read
        title="Antibiotic Frequency",
    )

    fig.update_layout(
        height=500,
        yaxis=dict(automargin=True),
    )

    st.plotly_chart(fig, use_container_width=True)

def organism_frequency(df: pd.DataFrame):
    st.subheader("Organism Frequency")

    df_org = (
        df.groupby("Organism")["Resistance_Level"]
        .count()
        .reset_index()
        .rename(columns={"Resistance_Level": "Count"})
        .sort_values("Count", ascending=False)
    )

    fig = px.bar(
        df_org,
        x="Count",
        y="Organism",
        orientation="h",
        title="Organism Frequency",
    )

    fig.update_layout(
        height=500,
        yaxis=dict(automargin=True),
    )

    st.plotly_chart(fig, use_container_width=True)

# Line chart representing the resistance trends of each antibiotic
def resistance_trends_by_antibiotic(df):
    if "Year" not in df.columns:
        st.warning("No Year column available for trend plots.")
        return
    
    fig = px.line(
        df,
        x="Year",
        y="MIC_Value",
        color="Antibiotic",
        markers=True,
        title="MIC Trends by Antibiotic"
    )
    st.plotly_chart(fig, use_container_width=True)

# Pie chart of the different resistance mechanisms in CARD
def card_mechanism_summary(df):
    st.subheader("Mechanism Distribution")
    counts = df["Resistance_Mechanism"].value_counts().reset_index()
    counts.columns = ["mechanism", "count"]

    fig = px.pie(counts, names="mechanism", values="count", title="Mechanism Frequency")
    st.plotly_chart(fig, use_container_width=True)

# Bar chart of the distribution of the antibiotics' drug classes 
def card_drugclass_distribution(df):
    st.subheader("Drug Class Distribution")
    counts = df["drug_class"].value_counts().reset_index()
    counts.columns = ["drug_class", "count"]

    fig = px.bar(
        counts,
        x="drug_class",
        y="count",
        title="CARD Drug Class Counts"
    )
    st.plotly_chart(fig, use_container_width=True)

# Bar chart of the distribution of the resistance genes
def card_gene_frequency(df):
    st.subheader("Gene Frequency")
    counts = df["gene"].value_counts().reset_index()
    counts.columns = ["gene", "count"]

    fig = px.bar(
        counts,
        x="gene",
        y="count",
        title="Most Common Resistance Genes"
    )
    st.plotly_chart(fig, use_container_width=True)

# Bar chart for country-level resistance summaries
def geography_country_summary(df: pd.DataFrame):
    st.subheader("Resistance by Country")

    if "Country" not in df.columns:
        st.info("No Country column available in dataset.")
        return

    df_country = (
        df.groupby("Country")["Resistance_Level"]
        .count()
        .reset_index()
        .rename(columns={"Resistance_Level": "Count"})
        .sort_values("Count", ascending=False)
    )

    fig = px.bar(
        df_country,
        x="Count",
        y="Country",
        orientation="h",
        title="Resistance Reports by Country",
    )

    fig.update_layout(
        height=500,
        yaxis=dict(automargin=True),
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_country)

# Bar chart for region-level resistance summaries
def geography_region_summary(df: pd.DataFrame):
    st.subheader("🌍 Resistance by Region")

    if "Region" not in df.columns:
        st.info("No Region column available in dataset.")
        return

    df_region = (
        df.groupby("Region")["Resistance_Level"]
        .count()
        .reset_index()
        .rename(columns={"Resistance_Level": "Count"})
        .sort_values("Count", ascending=False)
    )

    fig = px.bar(
        df_region,
        x="Count",
        y="Region",
        orientation="h",
        title="Resistance Reports by Region",
    )

    fig.update_layout(
        height=500,
        yaxis=dict(automargin=True),
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_region)