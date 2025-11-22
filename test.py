from sqlalchemy import create_engine, inspect

engine = create_engine("sqlite:///amr.db")
insp = inspect(engine)

print(insp.get_columns("card_genes"))