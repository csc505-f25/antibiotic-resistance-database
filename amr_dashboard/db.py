from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///amr.db")

# Connect to the search engine and run the queries
def run_query(query, params=None):
    with engine.connect() as conn:
        result = conn.execute(text(query), params or {})
        return result.fetchall()

def get_resistance_data(organism=None, antibiotic=None, region=None):
    query = """
    SELECT o.name as organism, a.name as antibiotic, r.region, r.year, r.resistance_level, r.mic_value
    FROM resistance_profiles r
    JOIN organisms o ON r.organism_id = o.organism_id
    JOIN antibiotics a ON r.antibiotic_id = a.antibiotic_id
    WHERE 1=1
    """
    params = {}
    if organism:
        query += " AND o.name = :organism"
        params["organism"] = organism
    if antibiotic:
        query += " AND a.name = :antibiotic"
        params["antibiotic"] = antibiotic
    if region:
        query += " AND r.region = :region"
        params["region"] = region

    return run_query(query, params)
