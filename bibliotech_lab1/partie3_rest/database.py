import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# En local : localhost. Dans Docker Compose, "db" est le nom du service Postgres
# (voir docker-compose.yml) — la variable d'environnement DATABASE_URL le gère.
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://library:library@localhost:5432/library"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dépendance FastAPI : ouvre une session par requête, la ferme après."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
