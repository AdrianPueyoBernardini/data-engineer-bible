from __future__ import annotations

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

try:
    from config import load_config
    from models import Base
except ModuleNotFoundError:  # pragma: no cover - fallback para importación como paquete.
    from src.config import load_config
    from src.models import Base


def ensure_database_exists() -> str:
    """Crea la base de laboratorio solo si el nombre termina en _lab y no existe ya."""
    cfg = load_config()
    db_name = cfg["dbname"]
    if not db_name.endswith("_lab"):
        raise ValueError(
            f"La base '{db_name}' no es segura para esta práctica. Debe terminar en '_lab'."
        )

    root_url = (
        f"postgresql+psycopg://{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/postgres"
    )
    root_engine = create_engine(root_url, future=True)

    with root_engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
        exists = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :dbname"),
            {"dbname": db_name},
        ).fetchone()

        if exists is None:
            conn.execute(text(f'CREATE DATABASE "{db_name}"'))
            print(f"[OK] Base creada: {db_name}")
        else:
            print(f"[OK] Base existente: {db_name}")

    return db_name


def prepare_schema() -> None:
    """Abre una Session y crea el esquema de la base de laboratorio.

    La Session se gestiona con `with Session(engine) as session:` para demostrar quién la posee,
    qué ocurre si falla una operación y cuándo se cierra la conexión. La creación real del esquema
    se delega a `engine.begin()` porque ahí SQLAlchemy puede emitir `CREATE TABLE` con la
    semántica de transacción de PostgreSQL de manera fiable.
    """
    cfg = load_config()
    url = (
        f"postgresql+psycopg://{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/{cfg['dbname']}"
    )
    engine = create_engine(url, echo=False, future=True)

    with Session(engine) as session:
        # La sesión demuestra el contexto normal: se abre, se usa y se cierra.
        session.execute(text("SELECT 1"))
        print(f"[OK] Session abierta y cerrada correctamente en {cfg['dbname']}")

    with engine.begin() as conn:
        Base.metadata.create_all(bind=conn)
        print(f"[OK] Esquema creado en {cfg['dbname']}")


def main() -> None:
    db_name = ensure_database_exists()
    prepare_schema()
    print(f"[INFO] Base lista para uso: {db_name}")


if __name__ == "__main__":
    main()
