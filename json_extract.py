import json
import csv

# Your AAC genes of interest
TARGET_GENES = [
    "AAC(2')-IIb", "AAC_3Ib_AAC_6Ib", "AAC(6')-Ib-Suzhou", "AAC(2')-Ia",
    "AAC(2')-Ic", "AAC(2')-Id", "AAC(2')-Ie", "AAC(2')-IIa", "AAC(3)-Ia",
    "AAC(3)-Ic", "AAC(3)-Id", "AAC(3)-IIa", "AAC(3)-IIb", "AAC(3)-IIc",
    "AAC(3)-IId", "AAC(3)-IIe", "AAC(3)-IIg", "AAC(3)-IIIa", "AAC(3)-IIIb",
    "AAC(3)-IIIc", "AAC(3)-IVa", "AAC(3)-IVb", "AAC(3)-IXa", "AAC(3)-VIa",
    "AAC(3)-VIIa", "AAC(3)-VIIIa", "AAC(3)-Xa", "AAC(6')-29a", "AAC(6')-29b",
    "AAC(6')-31", "AAC(6')-32", "AAC(6')-34", "AAC(6')-I-43", "AAC(6')-I-48",
    "AAC(6')-I30", "AAC(6')-I33", "AAC(6')-Ia", "AAC(6')-Iaa", "AAC(6')-Iad",
    "AAC(6')-Iae", "AAC(6')-Iaf"
]

# Input your JSON filename here
CARD_JSON_PATH = "data/card-data/card.json"
OUTPUT_CSV = "aac_genes.csv"

def main():
    # Load JSON
    with open(CARD_JSON_PATH, "r") as f:
        data = json.load(f)

    print("Loaded JSON keys:", data.keys())

    # CARD usually stores genes here:
    models = data.get("models", {})
    print(list(models.items())[:5])


    # Prepare output rows
    rows = []

    for aro_id, entry in models.items():
        model_name = entry.get("model_name", "")

        if model_name in TARGET_GENES:
            rows.append({
                "gene": model_name,
                "aro_id": aro_id,
                "description": entry.get("model_description", ""),
                "drug_class": "; ".join(entry.get("drug_class", [])),
                "resistance_mechanism": ": ".join(entry.get("resistance_mechanism", [])),
            })

    # Write CSV
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["gene", "aro_id", "description", "drug_class", "resistance_mechanism"]
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"[+] Extracted {len(rows)} AAC genes into {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
