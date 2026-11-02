#configparser para lectura de archivos
#path para manejar rutas
#psycopg es el conector entre Python y PostgreSQL
import configparser
from pathlib import Path

import psycopg

ROOT = Path(__file__).resolve().parent.parent


def leer_config(ruta=ROOT / "config.ini"):
    cfg = configparser.ConfigParser()
    if not cfg.read(ruta):
        raise FileNotFoundError(
            "No encuentro la ruta" + ruta.name
        )
    return cfg["postgres"]

def abrir_conexion():
    c = leer_config()
    try:
        return psycopg.connect(
            host=c["host"],
            port=c["port"],
            dbname=c["dbname"],
            user=c["user"],
            password=c["password"]
        )
    except psycopg.OperationalError as e:
        raise ConnectionError(
            f"No se pudo conectar a {c['host']}:{c['port']}/{c['dbname']} "
            f"como {c['user']}. ¿Está el servidor arrancado? Motivo: "
            f"{str(e).splitlines()[0]}"
        ) from None

