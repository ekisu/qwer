from sqlalchemy.engine.base import Engine
from qwer.database.engine import engine
from qwer.domain.entities import mapper_registry

def setup_database(engine: Engine):
    mapper_registry.metadata.create_all(engine)

if __name__ == "__main__":
    setup_database(engine)

    print('Database tables created successfully!')
