import pandas as pd

# Load your resistance gene CSV
genes = pd.read_csv("data/resistance_genes.csv")

# Load CARD ontology TSV
aro = pd.read_csv("data/card-ontology/aro.tsv", sep="\t")

# Make sure column names are stripped of whitespace
genes.columns = genes.columns.str.strip()
aro.columns = aro.columns.str.strip()

print(aro.columns)

# Ensure consistent accession format (CARD sometimes uses underscore)
aro["Accession"] = aro["Accession"].str.replace("_", ":", regex=False)

# Merge on the correct column
merged = genes.merge(
    aro[["Accession", "Description"]],   # just pull what you need
    how="left",
    left_on="aro_accession",
    right_on="Accession"
)

# Fill missing description using ontology Description
merged["description"] = merged["description"].fillna(merged["Description"])

# Drop the temporary Description and duplicate Accession
merged = merged.drop(columns=["Description", "Accession"], errors="ignore")

# Write clean output
merged.to_csv("data/resistance_genes_filled.csv",
              index=False)

print("✅ Done — saved resistance_genes_filled.csv with no duplicate columns.")
