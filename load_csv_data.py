import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///amr.db")

# File paths
antibiotics_csv = "data/antibiotics.csv"
bacteria_csv = "data/bacteria_taxonomy.csv"
drug_classes_csv = "data/drug_classes.csv"
resistance_csv = "data/card-data/card_flat.csv"

# Load CSVs
df_antibiotics = pd.read_csv(antibiotics_csv)
df_bacteria = pd.read_csv(bacteria_csv)
df_drug_classes = pd.read_csv(drug_classes_csv)
df_resistance = pd.read_csv(resistance_csv)

# === Base tables ===
df_drug_classes.to_sql("drug_classes", con=engine, if_exists="append", index=False)
df_antibiotics.to_sql("antibiotics", con=engine, if_exists="append", index=False)

# Organisms
df_organisms = df_bacteria.rename(columns={"bacteria_name": "name", "tax_id": "taxonomy_id"})[["name", "taxonomy_id"]]
df_organisms.to_sql("organisms", con=engine, if_exists="append", index=False)

# === Insert unique genes and mechanisms from CARD ===
df_genes = pd.DataFrame({"name": df_resistance["Gene"].dropna().unique()})
df_genes.to_sql("resistance_genes", con=engine, if_exists="append", index=False)

df_mechs = pd.DataFrame({"name": df_resistance["Resistance_Mechanism"].dropna().unique()})
df_mechs.to_sql("resistance_mechanisms", con=engine, if_exists="append", index=False)

# === Build mapping dicts ===
with engine.connect() as conn:
    antibiotics_map = pd.read_sql("SELECT antibiotic_id, name FROM antibiotics", conn).set_index("name")["antibiotic_id"].to_dict()
    organisms_map = pd.read_sql("SELECT organism_id, name FROM organisms", conn).set_index("name")["organism_id"].to_dict()
    genes_map = pd.read_sql("SELECT gene_id, name FROM resistance_genes", conn).set_index("name")["gene_id"].to_dict()
    mech_map = pd.read_sql("SELECT mechanism_id, name FROM resistance_mechanisms", conn).set_index("name")["mechanism_id"].to_dict()

# === Normalize names for matching ===
def normalize(x):
    if pd.isna(x): return None
    return x.strip().lower()

df_resistance["Organism_norm"] = df_resistance["Organism"].apply(normalize)
df_resistance["Antibiotics_norm"] = df_resistance["Antibiotics"].apply(normalize)
df_resistance["Gene_norm"] = df_resistance["Gene"].apply(normalize)
df_resistance["Mech_norm"] = df_resistance["Resistance_Mechanism"].apply(normalize)

# Normalize map keys
antibiotics_map_norm = {k.lower(): v for k, v in antibiotics_map.items()}
organisms_map_norm = {k.lower(): v for k, v in organisms_map.items()}
genes_map_norm = {k.lower(): v for k, v in genes_map.items()}
mech_map_norm = {k.lower(): v for k, v in mech_map.items()}

# === Map relationships ===
df_res = pd.DataFrame()
df_res["organism_id"] = df_resistance["Organism_norm"].map(organisms_map_norm)
df_res["antibiotic_id"] = df_resistance["Antibiotics_norm"].map(antibiotics_map_norm)
df_res["gene_id"] = df_resistance["Gene_norm"].map(genes_map_norm)
df_res["mechanism_id"] = df_resistance["Mech_norm"].map(mech_map_norm)

# Optional fields
for col in ["mic_value", "mic_unit", "resistance_level", "year", "region", "source_id"]:
    df_res[col] = None

# Drop unmapped rows
before = len(df_res)
df_res = df_res.dropna(subset=["organism_id", "antibiotic_id", "gene_id", "mechanism_id"])
after = len(df_res)

# Insert into DB
df_res.to_sql("resistance_profiles", con=engine, if_exists="append", index=False)

print(f"✅ Loaded resistance_profiles: {after}/{before} rows successfully mapped.")
