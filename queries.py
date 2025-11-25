from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///amr.db")

def run_query(query, params=None):
    with engine.connect() as conn:
        result = conn.execute(text(query), params or {})
        return result.fetchall()

print("=== AMR DATABASE SUMMARY REPORT ===\n")

# 1️⃣ Top 10 organisms by number of resistance entries
print("Top 10 organisms by resistance entries:")
query = """
SELECT o.name, COUNT(*) as resistance_count
FROM resistance_profiles r
JOIN organisms o ON r.organism_id = o.organism_id
GROUP BY o.name
ORDER BY resistance_count DESC
LIMIT 10
"""
results = run_query(query)
for name, count in results:
    print(f"{name}: {count}")
print()

# 2️⃣ Top 10 antibiotics by resistance entries
print("Top 10 antibiotics by resistance entries:")
query = """
SELECT a.name, COUNT(*) as resistance_count
FROM resistance_profiles r
JOIN antibiotics a ON r.antibiotic_id = a.antibiotic_id
GROUP BY a.name
ORDER BY resistance_count DESC
LIMIT 10
"""
results = run_query(query)
for name, count in results:
    print(f"{name}: {count}")
print()

# 3️⃣ Top 10 resistance mechanisms by number of organisms affected
print("Top 10 resistance mechanisms by organisms affected:")
query = """
SELECT m.name, COUNT(DISTINCT r.organism_id) as num_organisms
FROM resistance_profiles r
JOIN resistance_mechanisms m ON r.mechanism_id = m.mechanism_id
GROUP BY m.name
ORDER BY num_organisms DESC
LIMIT 10
"""
results = run_query(query)
for name, count in results:
    print(f"{name}: {count}")
print()

# 4️⃣ Top 10 genes by resistance entries
print("Top 10 resistance genes by entries:")
query = """
SELECT g.name, COUNT(*) as resistance_count
FROM resistance_profiles r
JOIN resistance_genes g ON r.gene_id = g.gene_id
GROUP BY g.name
ORDER BY resistance_count DESC
LIMIT 10
"""
results = run_query(query)
for name, count in results:
    print(f"{name}: {count}")
print()

print("=== END OF REPORT ===")
