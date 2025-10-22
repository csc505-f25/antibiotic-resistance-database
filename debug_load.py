import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///amr.db")

# Load CARD data
df = pd.read_csv("data/card-data/card_flat.csv")
print("CARD sample:")
print(df.head(5))
print("\nUnique counts:")
print({
    "Organism": df["Organism"].nunique(),
    "Antibiotics": df["Antibiotics"].nunique(),
    "Gene": df["Gene"].nunique(),
    "Mechanism": df["Resistance_Mechanism"].nunique()
})

# Load what’s in DB
with engine.connect() as conn:
    orgs = pd.read_sql("SELECT name FROM organisms", conn)
    abx = pd.read_sql("SELECT name FROM antibiotics", conn)
    genes = pd.read_sql("SELECT name FROM resistance_genes", conn)
    mechs = pd.read_sql("SELECT name FROM resistance_mechanisms", conn)

print("\nOrganisms in DB:", len(orgs))
print("Antibiotics in DB:", len(abx))
print("Genes in DB:", len(genes))
print("Mechanisms in DB:", len(mechs))

# Find example mismatches
sample_org = df["Organism"].dropna().iloc[0]
print("\nSample CARD organism:", sample_org)
matches = orgs[orgs["name"].str.contains(sample_org.split()[0], case=False, na=False)]
print(f"Closest matches for '{sample_org}':")
print(matches.head())
