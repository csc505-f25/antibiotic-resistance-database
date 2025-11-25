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

2. **Run the run_app.sh script.**

```bash
./run_app.sh
```
