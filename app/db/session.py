from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL
from sqlalchemy.orm import declarative_base
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
Base = declarative_base()
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)