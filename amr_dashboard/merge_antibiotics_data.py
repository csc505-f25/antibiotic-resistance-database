import pandas as pd

# File paths
ANTIBIOTICS_CSV = "/Users/emilylight/Desktop/CSC505/antibiotic-resistance-database/data/antibiotics.csv"
RESISTANCE_PROFILE_TSV = "/Users/emilylight/Desktop/CSC505/antibiotic-resistance-database/data/resistance_profiles.tsv"
OUTPUT_TSV = "/Users/emilylight/Desktop/CSC505/antibiotic-resistance-database/data/resistance_profiles_updated.tsv"

# Load files
ab_df = pd.read_csv(ANTIBIOTICS_CSV)  # should have columns: antibiotic_id, name
rp_df = pd.read_csv(RESISTANCE_PROFILE_TSV, sep="\t")  # should have column: Antibiotic
ab_names = ab_df['name'].to_list()
ab_ids = ab_df['antibiotic_id'].to_list()

for idx, row in rp_df.iterrows():
    ab_name = str(row['Antibiotic']).strip().lower()
    if ab_name in ab_names:
        pos = ab_names.index(ab_name)
        ab_id = ab_ids[pos]
        rp_df.at[idx, 'antibiotic_id'] = int(ab_id)
        print(f"Matched {ab_name} -> ID {ab_id} at row {idx}")
    else:
        print(f"No match for {ab_name} at row {idx}")


print(f"Updated resistance profiles saved to {OUTPUT_TSV}")
