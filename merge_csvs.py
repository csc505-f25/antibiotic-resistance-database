import pandas as pd

# Paths to your CSVs
csv1 = "/Users/emilylight/Desktop/CSC505/antibiotic-resistance-database/data/bacteria_taxonomy.csv"
csv2 = "/Users/emilylight/Desktop/CSC505/antibiotic-resistance-database/ncbi_missing_organisms.csv"

# Read CSVs
df1 = pd.read_csv(csv1)
df2 = pd.read_csv(csv2)

# Merge by 'name', keeping all rows from both CSVs
merged_df = pd.merge(df1, df2, on="name", how="outer", suffixes=('_1', '_2'))

# Optional: resolve conflicts
# For example, prefer tax_id from df1 if exists, else from df2
merged_df['tax_id'] = merged_df['tax_id_1'].combine_first(merged_df['tax_id_2'])
merged_df['rank'] = merged_df['rank_1'].combine_first(merged_df['rank_2'])
merged_df['lineage'] = merged_df['lineage_1'].combine_first(merged_df['lineage_2'])
merged_df['division'] = merged_df['division_1'].combine_first(merged_df['division_2'])

# Keep only necessary columns
merged_df = merged_df[['name', 'tax_id', 'rank', 'lineage', 'division']]

# Sort alphabetically by name
merged_df = merged_df.sort_values(by='name').reset_index(drop=True)

# Save merged CSV
merged_df.to_csv("/Users/emilylight/Desktop/CSC505/antibiotic-resistance-database/bacteria_merged_sorted.csv", index=False)

print("Merged CSV saved to merged_sorted.csv")
