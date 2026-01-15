import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Try to use DATABASE_URL directly if present
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    POSTGRES_USER = os.getenv("DB_USER")
    POSTGRES_PASSWORD = os.getenv("DB_PASSWORD")
    POSTGRES_DB = os.getenv("DB_NAME")
    POSTGRES_HOST = os.getenv("DB_HOST")
    POSTGRES_PORT = os.getenv("DB_PORT")

    # Debug print to help diagnose issues
    print("DB_USER:", POSTGRES_USER)
    print("DB_PASSWORD:", POSTGRES_PASSWORD)
    print("DB_NAME:", POSTGRES_DB)
    print("DB_HOST:", POSTGRES_HOST)
    print("DB_PORT:", POSTGRES_PORT)

    # Fallback to default port if not set
    if not POSTGRES_PORT or POSTGRES_PORT == 'None':
        POSTGRES_PORT = '5432'

    DATABASE_URL = (
        f"postgresql://{POSTGRES_USER}:"
        f"{POSTGRES_PASSWORD}@"
        f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
