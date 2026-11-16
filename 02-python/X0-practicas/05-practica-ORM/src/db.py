from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .config import load_config

cfg = load_config()
url = (
    f"postgresql+psycopg://{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/{cfg['dbname']}"
)

echo_sql = os.getenv("SQL_ECHO", "0") == "1"
engine = create_engine(url, echo=echo_sql, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, future=True)


def get_session() -> Session:
    """Devuelve una sesión SQLAlchemy para un bloque de trabajo."""
    return SessionLocal()
