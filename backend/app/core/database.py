from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# IMPORTANTE: Nota el +psycopg en la URL para usar psycopg3
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:0407@localhost:5432/sigpp_unicartagena"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=True  # Para debug, cambiar a False en producción
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

