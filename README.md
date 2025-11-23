# AMR Resistance Dashboard

A **Streamlit dashboard** for exploring **antimicrobial resistance (AMR) data**, integrating phenotypic resistance profiles and genotype-based resistance information from the CARD database.

This dashboard allows users to:

- Query resistance profiles by organism, antibiotic, region, and resistance level.
- Visualize trends over time and geographic distribution.
- Explore CARD genes, mechanisms, and drug classes.
- Generate summary charts for resistance patterns and gene frequency.

---

## Features

### Phenotypic Resistance (Resistance Profiles)
- Search by organism, antibiotic, and location.
- Filter by resistance level: susceptible, intermediate, resistant.
- Interactive data table with row selection.
- Visualizations:
  - Resistance level distribution
  - Trends over time
  - Geographic summaries
  - Antibiotic and organism frequency

### Genotype Resistance (CARD)
- Search by organism, gene, or resistance mechanism.
- View CARD gene details, drug class, and mechanism.
- Explore unique values for each column.
- Summary charts for:
  - Mechanism distribution
  - Drug class distribution
  - Gene frequency

---

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/csc505-f25/antibiotic-resistance-database.git
cd antibiotic-resistance-database
```

2. **Insall the package locally:
```bash
pip install -e .
```

3. Install required dependencies if not already installed:
```bash
pip install streamlit pandas sqlalchemy streamlit-aggrid
```

## Running the App
Run the Streamlit app with:
```bash
streamlit run amr_dashboard/app.py
```
Then open your browser at http://localhost:8501.