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