import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from typing import Generator
from app.core.config import settings

DATABASE_URL = os.getenv(
    settings.database.url,
    "postgresql+psycopg://taskflow:taskflow@localhost:5432/taskflow",
)

engine = create_engine(
    settings.database.url,
    echo=settings.debug,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Base(DeclarativeBase):
    pass