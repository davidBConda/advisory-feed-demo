import os
from pathlib import Path

from dotenv import load_dotenv
from sqlmodel import Session, create_engine

load_dotenv()

DEFAULT_DB_PATH = Path(__file__).parent / "advisories.db"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def get_session() -> Session:
    return Session(engine)
