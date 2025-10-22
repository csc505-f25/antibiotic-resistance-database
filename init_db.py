from sqlalchemy import create_engine, text

# Create a new SQLite database file (or connect if it exists)
engine = create_engine("sqlite:///amr.db")

# Read the SQL schema from file
with open("schema_sqlite.sql") as f:
    schema_sql = f.read()

# Execute the schema to create all tables
with engine.connect() as conn:
    for statement in schema_sql.split(";"):
        stmt = statement.strip()
        if stmt:
            conn.execute(text(stmt))
    conn.commit()

print(" Database initialized and amr.db created successfully.")
