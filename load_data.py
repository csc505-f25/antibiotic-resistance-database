import pandas as pd
from sqlalchemy import create_engine
import re

engine = create_engine("sqlite:///amr.db")

# === File paths ===
card_csv = "data/card-data/card_flat.csv"
profiles_tsv = "data/resistance_profiles.tsv"

# === Load datasets ===
df_card = pd.read_csv(card_csv)
df_profiles = pd.read_csv(profiles_tsv, sep="\t")

# CARD → card_genes
df_card_genes = df_card.rename(columns={
    "ARO_ID": "aro_id",
    "Gene": "gene",
    "Organism": "organism",
    "Antibiotics": "antibiotics",
    "Drug_Class": "drug_class",
    "Resistance_Mechanism": "mechanism",
})

df_card_genes.to_sql("card_genes", engine, if_exists="replace", index=False)
print(f"Loaded card_genes: {len(df_card_genes)} rows")

# ================================
# 2️⃣ NCBI profiles → resistance_profiles
# ================================
df_profiles = df_profiles.rename(columns={
    "#BioSample": "biosample",
    "Organism group": "organism_group",
    "Scientific name": "scientific_name",
    "Isolation type": "isolation_type",
    "Location": "location",
    "Isolation source": "isolation_source",
    "Isolate": "isolate",
    "Antibiotic": "antibiotic",
    "Resistance phenotype": "resistance_phenotype",
    "Measurement sign": "measurement_sign",
    "MIC (mg/L)": "mic_mg_L",
    "Disk diffusion (mm)": "disk_diffusion_mm",
    "Laboratory typing platform": "lab_platform",
    "Vendor": "vendor",
    "Laboratory typing method version or reagent": "method_version",
    "Testing standard": "testing_standard",
    "Create date": "create_date"
})

# Validate the ISO format: YYYY-MM-DDTHH:MM:SSZ
iso_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

# Mark invalid timestamps
invalid_dates = df_profiles[~df_profiles["create_date"].astype(str).str.match(iso_pattern)]
if len(invalid_dates) > 0:
    print("⚠️ Invalid date rows found:")
    print(invalid_dates[["create_date"]].head())
else:
    print("All create_date values match ISO-8601 format.")

# Convert to datetime and extract YEAR
df_profiles["create_date"] = pd.to_datetime(df_profiles["create_date"], errors="coerce")
df_profiles["year"] = df_profiles["create_date"].dt.year

# Report how many failed conversion
num_errors = df_profiles["create_date"].isna().sum()
if num_errors > 0:
    print(f"⚠️ {num_errors} rows have invalid dates and were set to NaT.")

# Save to database
df_profiles.to_sql("resistance_profiles", engine, if_exists="replace", index=False)
print(f"Loaded resistance_profiles: {len(df_profiles)} rows")
print("Columns now include: year")