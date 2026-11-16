import configparser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config.ini"


def load_config() -> dict[str, str]:
    """Carga la configuración del acceso a PostgreSQL desde config.ini."""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"Falta {CONFIG_PATH.name}. Copia config.ini.example a config.ini y rellena los valores reales."
        )

    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH, encoding="utf-8")

    if "postgres" not in parser:
        raise KeyError("La sección [postgres] no existe en config.ini")

    section = parser["postgres"]
    required = ["host", "port", "dbname", "user", "password"]
    missing = [name for name in required if not section.get(name, "").strip()]
    if missing:
        raise ValueError(f"config.ini tiene valores vacíos: {', '.join(missing)}")

    return {
        "host": section["host"],
        "port": section["port"],
        "dbname": section["dbname"],
        "user": section["user"],
        "password": section["password"],
    }
