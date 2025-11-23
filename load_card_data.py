import sqlite3
import pandas as pd

DB = "amr.db"
CSV = "data/card-data/card_flat.csv"

conn = sqlite3.connect(DB)
cursor = conn.cursor()

df = pd.read_csv(CSV)

# Map table names to primary key column names
PRIMARY_KEYS = {
    "organisms": "organism_id",
    "antibiotics": "antibiotic_id",
    "drug_classes": "drug_class_id",
    "resistance_genes": "resistance_gene_id",
    "resistance_mechanisms": "resistance_mechanism_id"
}

# Helpers to get-or-create id lookups
def get_or_insert(table, col, value):
    pk = PRIMARY_KEYS[table]
    cursor.execute(f"SELECT {pk} FROM {table} WHERE {col} = ?", (value,))
    row = cursor.fetchone()
    if row:
        return row[0]
    cursor.execute(f"INSERT INTO {table} ({col}) VALUES (?)", (value,))
    return cursor.lastrowid

count_profiles = 0

for _, row in df.iterrows():
    # Validate organism
    org = row["Organism"]
    if pd.isna(org) or not str(org).strip():
        print("⚠️ Skipping row with missing Organism:", row.to_dict())
        continue

    organism_id = get_or_insert("organisms", "name", str(org).strip())

    gene_id = get_or_insert("resistance_genes", "name", row["Gene"])
    mechanism_id = get_or_insert("resistance_mechanisms", "name", row["Resistance_Mechanism"])

    # Split semicolon lists
    antibiotics = str(row["Antibiotics"]).split(";") if pd.notna(row["Antibiotics"]) else []
    drug_classes = str(row["Drug_Class"]).split(";") if pd.notna(row["Drug_Class"]) else []

    for dc in drug_classes:
        dc = dc.strip()
        if not dc:
            continue
        get_or_insert("drug_classes", "name", dc)

    for ab in antibiotics:
        ab = ab.strip()
        if not ab:
            continue

        # link antibiotic with drug class? simplified
        antibiotic_id = get_or_insert("antibiotics", "name", ab)

        # create resistance profile entry
        cursor.execute("""
            INSERT INTO resistance_profiles (organism_id, antibiotic_id, resistance_gene_id, resistance_mechanism_id)
            VALUES (?, ?, ?, ?)
        """, (organism_id, antibiotic_id, gene_id, mechanism_id))
        count_profiles += 1

conn.commit()
conn.close()

print(f"✅ Loaded {count_profiles} resistance profiles from CARD data")
