import sqlite3

DB = "amr.db"

def query_resistance(organism=None, antibiotic=None, region=None):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    query = """
        SELECT 
            o.name AS organism,
            a.name AS antibiotic,
            d.name AS drug_class,
            s.name AS source,
            rp.year,
            rp.region,
            rp.resistance_level
        FROM resistance_profiles rp
        JOIN organisms o ON rp.organism_id = o.organism_id
        JOIN antibiotics a ON rp.antibiotic_id = a.antibiotic_id
        LEFT JOIN drug_classes d ON a.drug_class_id = d.drug_class_id
        LEFT JOIN data_sources s ON rp.source_id = s.source_id
        WHERE 1=1
    """

    params = []

    if organism:
        query += " AND o.name LIKE ?"
        params.append(f"%{organism}%")

    if antibiotic:
        query += " AND a.name LIKE ?"
        params.append(f"%{antibiotic}%")

    if region:
        query += " AND rp.region LIKE ?"
        params.append(f"%{region}%")

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results
