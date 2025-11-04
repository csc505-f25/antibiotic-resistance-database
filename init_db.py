from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///amr.db")

with engine.begin() as conn:  # <-- begin auto-commits
    with open("schema_sqlite.sql") as f:
        schema_sql = f.read()

    for statement in schema_sql.split(";"):
        stmt = statement.strip()
        if stmt:
            conn.execute(text(stmt))

print("✅ Database initialized and amr.db created successfully.")
