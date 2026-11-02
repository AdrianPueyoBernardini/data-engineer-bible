from datetime import date

from db import abrir_conexion
from repositorio import Ruta, crear_ruta
from repositorio_planes import Plan
from importador import importar_planes, existe_operacion


def estado(conn):
    """Lee el estado real de la base con la conexión que se le pase."""
    with conn.cursor() as cur:
        cur.execute("SELECT id_plan FROM plan_viaje ORDER BY id_plan")
        planes = [f[0] for f in cur.fetchall()]
        cur.execute("SELECT count(*) FROM resumen_importacion")
        resumenes = cur.fetchone()[0]
    return planes, resumenes


def leer_desde_otra_conexion():
    otra = abrir_conexion()
    try:
        return estado(otra)
    finally:
        otra.close()


conn = abrir_conexion()
try:
    # Base: una ruta y un plan previo ya confirmados (el "B01" y el "R01")
    crear_ruta(conn, Ruta("TX01", "Ruta de transaccion", 10.0, 500, "Ordesa", "Media"))
    conn.commit()
    importar_planes(conn, [Plan("PREV", "TX01", date(2027, 6, 1), date(2027, 6, 2), "pendiente")])
    print("Estado inicial:      ", leer_desde_otra_conexion())

    lote = [
        Plan("PN1", "TX01", date(2027, 7, 1), date(2027, 7, 2), "pendiente"),
        Plan("PN2", "TX01", date(2027, 7, 8), date(2027, 7, 9), "pendiente"),
    ]

    # Ejecución con fallo forzado antes del commit
    try:
        importar_planes(conn, lote, fallo_prueba=True)
    except RuntimeError as e:
        print("Fallo capturado:     ", e)
    print("Tras el fallo:       ", leer_desde_otra_conexion())

    # Ejecución correcta
    id_operacion, res = importar_planes(conn, lote)
    print("Tras la correcta:    ", leer_desde_otra_conexion())
    otra = abrir_conexion()
    try:
        print("¿Existe la operación?", existe_operacion(otra, id_operacion))
    finally:
        otra.close()
finally:
    conn.close()