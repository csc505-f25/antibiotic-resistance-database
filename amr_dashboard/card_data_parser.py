import json
import pandas as pd

with open("data/card-data/card.json") as f:
    data = json.load(f)

rows = []
# ✅ Use .items() so we get (id, dict)
for model_id, model in data.items():
    if not isinstance(model, dict):
        continue  # skip if it's not a dictionary (safety check)

    gene = model.get("ARO_name")
    aro_id = model.get("ARO_accession")

    organism = None
    if "model_sequences" in model:
        seqs = model["model_sequences"].get("sequence", {})
        for _, s in seqs.items():
            if "NCBI_taxonomy" in s:
                organism = s["NCBI_taxonomy"].get("NCBI_taxonomy_name")
                break

    antibiotics, drug_classes, mechanisms = [], [], []
    for cat in model.get("ARO_category", {}).values():
        cls = cat.get("category_aro_class_name")
        if cls == "Antibiotic":
            antibiotics.append(cat.get("category_aro_name"))
        elif cls == "Drug Class":
            drug_classes.append(cat.get("category_aro_name"))
        elif cls == "Resistance Mechanism":
            mechanisms.append(cat.get("category_aro_name"))

    rows.append({
        "ARO_ID": aro_id,
        "Gene": gene,
        "Organism": organism,
        "Antibiotics": ";".join(antibiotics),
        "Drug_Class": ";".join(drug_classes),
        "Resistance_Mechanism": ";".join(mechanisms)
    })

df = pd.DataFrame(rows)
df.to_csv("card_flat.csv", index=False)
print("✅ Extracted", len(df), "records to card_flat.csv")
