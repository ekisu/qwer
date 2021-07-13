from sqlalchemy.engine import create_engine

engine = create_engine('sqlite:///database.db', future=True)
