import pandas as pd
from sqlalchemy import create_engine, inspect, text


engine = create_engine("sqlite:///amr.db")

insp = inspect(engine)
required = {"organisms", "antibiotics", "drug_classes"}
missing = required - set(insp.get_table_names())
if missing:
    raise RuntimeError(f"ERROR: Tables not created: {missing}. Run init_db.py first.")

# File paths
antibiotics_csv = "data/antibiotics.csv"
bacteria_csv = "data/bacteria_taxonomy.csv"
drug_classes_csv = "data/drug_classes.csv"
gene_families_csv = "data/gene_families.csv"
resistance_csv = "data/card-data/card_flat.csv"
resistance_profile_csv = "data/resistance_profiles_updated.tsv"

# Load CSVs
df_antibiotics = pd.read_csv(antibiotics_csv)
df_bacteria = pd.read_csv(bacteria_csv)
df_drug_classes = pd.read_csv(drug_classes_csv)
df_gene_families = pd.read_csv(gene_families_csv)
df_resistance = pd.read_csv(resistance_csv)
df_resistance_profiles = pd.read_csv(resistance_profile_csv, sep='\t')

# === Base tables ===
df_drug_classes.to_sql("drug_classes", con=engine, if_exists="replace", index=False)
print(f"✅ Loaded drug classes")

df_antibiotics.to_sql("antibiotics", con=engine, if_exists="replace", index=False)
print(f"✅ Loaded antibiotics")

# Organisms
df_organisms = df_bacteria.rename(columns={"bacteria_name": "name", "tax_id": "taxonomy_id"})[["name", "taxonomy_id"]]
df_organisms.to_sql("organisms", con=engine, if_exists="append", index=False)
print(f"✅ Loaded bacteria")

# === Insert unique genes and mechanisms ===
df_genes = pd.DataFrame({"name": df_resistance["Gene"].dropna().unique()})
df_genes.to_sql("resistance_genes", con=engine, if_exists="append", index=False)
print(f"✅ Loaded resistance genes")

df_mechs = pd.DataFrame({"name": df_resistance["Resistance_Mechanism"].dropna().unique()})
df_mechs.to_sql("resistance_mechanisms", con=engine, if_exists="append", index=False)
print(f"✅ Loaded resistance mechanisms")

# === Build mapping dicts ===
with engine.connect() as conn:
    antibiotics_map = pd.read_sql("SELECT antibiotic_id, name FROM antibiotics", conn).set_index("name")["antibiotic_id"].to_dict()
    organisms_map = pd.read_sql("SELECT organism_id, name FROM organisms", conn).set_index("name")["organism_id"].to_dict()
    genes_map = pd.read_sql("SELECT resistance_gene_id, name FROM resistance_genes", conn).set_index("name")["resistance_gene_id"].to_dict()
    mech_map = pd.read_sql("SELECT resistance_mechanism_id, name FROM resistance_mechanisms", conn).set_index("name")["resistance_mechanism_id"].to_dict()

# === Normalize ===
def normalize(x):
    if pd.isna(x): return None
    return x.strip().lower()

df_resistance["Organism_norm"] = df_resistance["Organism"].apply(normalize)
df_resistance["Antibiotics_norm"] = df_resistance["Antibiotics"].apply(normalize)
df_resistance["Gene_norm"] = df_resistance["Gene"].apply(normalize)
df_resistance["Mech_norm"] = df_resistance["Resistance_Mechanism"].apply(normalize)

# Normalized maps
antibiotics_map_norm = {k.lower(): v for k, v in antibiotics_map.items()}
organisms_map_norm = {k.lower(): v for k, v in organisms_map.items()}
genes_map_norm = {k.lower(): v for k, v in genes_map.items()}
mech_map_norm = {k.lower(): v for k, v in mech_map.items()}

# === Map relationships ===
df_res = pd.DataFrame()
df_res["organism_id"] = df_resistance["Organism_norm"].map(organisms_map_norm)
df_res["antibiotic_id"] = df_resistance["Antibiotics_norm"].map(antibiotics_map_norm)
df_res["resistance_gene_id"] = df_resistance["Gene_norm"].map(genes_map_norm)
df_res["resistance_mechanism_id"] = df_resistance["Mech_norm"].map(mech_map_norm)

# Optional null columns
for col in ["mic_value", "mic_unit", "resistance_level", "year", "region", "source_id"]:
    df_res[col] = None

# Drop rows missing required FKs
before = len(df_res)
df_res = df_res.dropna(subset=["organism_id", "antibiotic_id", "resistance_gene_id", "resistance_mechanism_id"])
after = len(df_res)

# Insert
df_res.to_sql("resistance_profiles", con=engine, if_exists="append", index=False)

print(f"✅ Loaded resistance_profiles: {after}/{before} rows successfully mapped.")