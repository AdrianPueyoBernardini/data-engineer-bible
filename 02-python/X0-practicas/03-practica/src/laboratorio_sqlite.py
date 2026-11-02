import sqlite3
import sys
from pathlib import Path

RUTA_BD = Path(__file__).resolve().parent.parent / "data" / "laboratorio.db"

ESQUEMA = """
CREATE TABLE IF NOT EXISTS ruta (
    id_ruta       TEXT PRIMARY KEY,
    nombre        TEXT NOT NULL,
    distancia_km  REAL NOT NULL CHECK (distancia_km > 0),
    desnivel_m    INTEGER CHECK (desnivel_m >= 0)
)
"""


def listar(conn):
    return conn.execute(
        "SELECT id_ruta, nombre, distancia_km, desnivel_m FROM ruta ORDER BY id_ruta"
    ).fetchall()


def preparar():
    # Estado conocido: se empieza siempre con un archivo nuevo
    if RUTA_BD.exists():
        RUTA_BD.unlink()

    conn = sqlite3.connect(RUTA_BD)
    try:
        print(f"Motor: SQLite {sqlite3.sqlite_version} (módulo sqlite3 de Python {sys.version.split()[0]})")
        conn.execute(ESQUEMA)

        # 1. Inserción (una ruta permanente y otra de prueba, con apóstrofo y desnivel ausente)
        sql_alta = (
            "INSERT INTO ruta (id_ruta, nombre, distancia_km, desnivel_m) "
            "VALUES (?, ?, ?, ?)"
        )
        conn.execute(sql_alta, ("L01", "Ibon de Plan", 8.5, 650))
        conn.execute(sql_alta, ("LT1", "Pico d'Aneto", 12.5, None))
        conn.commit()
        print("1. Insertadas:", listar(conn))

        # 2. Consulta por clave
        fila = conn.execute(
            "SELECT id_ruta, nombre, distancia_km, desnivel_m FROM ruta WHERE id_ruta = ?",
            ("LT1",),
        ).fetchone()
        print("2. Búsqueda por clave:", fila)

        # 3. Modificación
        cur = conn.execute(
            "UPDATE ruta SET distancia_km = ? WHERE id_ruta = ?", (9.0, "L01")
        )
        conn.commit()
        print("3. Filas modificadas:", cur.rowcount)

        # 4. Borrado del registro de prueba
        cur = conn.execute("DELETE FROM ruta WHERE id_ruta = ?", ("LT1",))
        conn.commit()
        print("4. Filas borradas:", cur.rowcount)

        # 5 y 6. El motor también rechaza datos inválidos
        try:
            conn.execute(sql_alta, ("L01", "Repetida", 5.0, 100))
        except sqlite3.IntegrityError as e:
            conn.rollback()
            print("5. Clave repetida rechazada:", e)
        try:
            conn.execute(sql_alta, ("L02", "Negativa", -3.0, 100))
        except sqlite3.IntegrityError as e:
            conn.rollback()
            print("6. Distancia negativa rechazada:", e)

        print("Antes de cerrar:", listar(conn))
    finally:
        conn.close()
    print("Conexión cerrada. Ahora ejecuta: python src/laboratorio_sqlite.py reabrir")


def reabrir():
    if not RUTA_BD.exists():
        raise SystemExit("No existe laboratorio.db: ejecuta primero 'preparar'.")
    conn = sqlite3.connect(RUTA_BD)
    try:
        print("Tras reabrir en otra ejecución:", listar(conn))
    finally:
        conn.close()


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else ""
    if modo == "preparar":
        preparar()
    elif modo == "reabrir":
        reabrir()
    else:
        raise SystemExit("Uso: python src/laboratorio_sqlite.py [preparar|reabrir]")