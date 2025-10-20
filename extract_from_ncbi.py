from Bio import Entrez
import time
from tqdm import tqdm
import csv

# NCBI email (required)
Entrez.email = "your_email@example.com"

# Read bacteria list from a file (one name per line)
bacteria_list = []
with open("bacteria_list.txt", "r") as f:
    for line in f:
        name = line.strip()
        if name:  # skip empty lines
            bacteria_list.append(name)
            
# Function to fetch taxonomy data
def fetch_taxonomy(bacterium):
    try:
        handle = Entrez.esearch(db="taxonomy", term=bacterium)
        record = Entrez.read(handle)
        handle.close()
        tax_id = record['IdList'][0] if record['IdList'] else None
        if tax_id:
            summary_handle = Entrez.efetch(db="taxonomy", id=tax_id)
            summary = Entrez.read(summary_handle)
            summary_handle.close()
            return summary[0]
        return None
    except Exception as e:
        print(f"Error fetching {bacterium}: {e}")
        return None

# Fetch data for all bacteria
bacteria_data = []
for b in tqdm(bacteria_list, desc="Fetching bacteria taxonomy"):
    data = fetch_taxonomy(b)
    if data:
        bacteria_data.append({
            "name": b,
            "tax_id": data.get("TaxId"),
            "rank": data.get("Rank"),
            "lineage": data.get("Lineage"),
            "division": data.get("Division")
        })
    time.sleep(0.3)  # polite delay to avoid NCBI rate limits


# Save results to CSV
csv_file = "bacteria_taxonomy.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "tax_id", "rank", "lineage", "division"])
    writer.writeheader()
    writer.writerows(bacteria_data)

print(f"Results saved to {csv_file}")