from Bio import Entrez
import csv
import time

# Set your email (NCBI requires this)
Entrez.email = "your_email@example.com"

# List of missing organisms

with open("missing_bacteria.txt", "r") as f:
    missing_organisms = [line.strip() for line in f if line.strip()]

# Output CSV file
output_file = "ncbi_missing_organisms.csv"

# Open CSV and write header
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Name", "TaxID", "Rank", "Lineage", "Division"])

    for org in missing_organisms:
        # Search taxonomy
        handle = Entrez.esearch(db="taxonomy", term=org)
        record = Entrez.read(handle)
        handle.close()
        time.sleep(0.3)  # polite delay for NCBI server

        if record["IdList"]:
            tax_id = record["IdList"][0]

            # Fetch taxonomy details
            handle = Entrez.efetch(db="taxonomy", id=tax_id, retmode="xml")
            tax_record = Entrez.read(handle)[0]
            handle.close()

            name = tax_record.get("ScientificName", "")
            rank = tax_record.get("Rank", "")
            lineage = tax_record.get("Lineage", "")
            division = tax_record.get("Division", "")

            writer.writerow([name, tax_id, rank, lineage, division])
        else:
            writer.writerow([org, "NOT FOUND", "", "", ""])
            print(f"Not found: {org}")
