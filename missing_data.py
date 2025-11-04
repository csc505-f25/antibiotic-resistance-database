import pandas as pd
from sqlalchemy import create_engine

# --- Connect to your DB ---
engine = create_engine("sqlite:///amr.db")

# --- Load CSV ---
card_csv = "data/card-data/card_flat.csv"
df_card = pd.read_csv(card_csv)

# --- Helper to get existing DB entries ---
def get_db_set(table, column):
    query = f"SELECT {column} FROM {table}"
    return set(pd.read_sql(query, engine)[column].str.lower().tolist())

# --- Current DB entries ---
db_organisms = get_db_set("organisms", "name")
db_antibiotics = get_db_set("antibiotics", "name")
db_genes = get_db_set("resistance_genes", "name")
db_mechanisms = get_db_set("resistance_mechanisms", "name")

# --- Unique values from CARD CSV ---
csv_organisms = set(df_card["Organism"].dropna().str.lower())
csv_antibiotics = set(
    df_card["Antibiotics"]
    .dropna()
    .str.lower()
    .str.split(";")
    .explode()
    .str.strip()
)

csv_genes = set(df_card["Gene"].dropna().str.lower())
csv_mechanisms = set(df_card["Resistance_Mechanism"].dropna().str.lower())

# --- Find missing entries ---
missing_organisms = csv_organisms - db_organisms
missing_antibiotics = csv_antibiotics - db_antibiotics
missing_genes = csv_genes - db_genes
missing_mechanisms = csv_mechanisms - db_mechanisms

# --- Output ---
print("❌ Missing Organisms:", len(missing_organisms))
for o in sorted(missing_organisms):
    print("  ", o)

print("\n❌ Missing Antibiotics:", len(missing_antibiotics))
for a in sorted(missing_antibiotics):
    print("  ", a)

print("\n❌ Missing Genes:", len(missing_genes))
for g in sorted(missing_genes):
    print("  ", g)

print("\n❌ Missing Mechanisms:", len(missing_mechanisms))
for m in sorted(missing_mechanisms):
    print("  ", m)
