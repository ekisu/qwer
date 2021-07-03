from qwer.database.engine import engine
from qwer.domain.entities import mapper_registry

if __name__ == "__main__":
    mapper_registry.metadata.create_all(engine)

    print('Database tables created successfully!')
