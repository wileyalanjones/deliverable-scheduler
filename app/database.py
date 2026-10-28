from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine(
    "sqlite:///./app.db", 
    connect_args={"check_same_thread": False},
    echo=True)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False,
    bind=engine
    )

class Base(DeclarativeBase):
    pass

