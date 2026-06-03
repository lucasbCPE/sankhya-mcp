from sqlalchemy import create_engine, inspect

engine = create_engine("mssql+pymssql://user:pass@host:1433/database")
insp = inspect(engine)
print(insp.get_table_names()[:10])  # deve listar algumas tabelas do Sankhya