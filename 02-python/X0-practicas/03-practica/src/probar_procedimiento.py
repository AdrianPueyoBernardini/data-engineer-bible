import psycopg

from db import abrir_conexion
from repositorio import (
    Ruta, crear_ruta, buscar_ruta, eliminar_ruta, renombrar_ruta_proc,
)


def nombre_desde_otra_conexion(id_ruta):
    otra = abrir_conexion()
    try:
        ruta = buscar_ruta(otra, id_ruta)
        return ruta.nombre if ruta else None
    finally:
        otra.close()


conn = abrir_conexion()
try:
    # Estado conocido: ruta de prueba independiente
    eliminar_ruta(conn, "TP01")
    conn.commit()
    crear_ruta(conn, Ruta("TP01", "Nombre original", 5.0, 100, "Ordesa", "Facil"))
    conn.commit()

    # 1. Llamada correcta, con apóstrofo, confirmada
    renombrar_ruta_proc(conn, "TP01", "Pico d'Aneto (renombrado)")
    conn.commit()
    print("1. Tras CALL y commit:", nombre_desde_otra_conexion("TP01"))

    # 2. Identidad inexistente
    try:
        renombrar_ruta_proc(conn, "NOEXISTE", "Cualquiera")
    except psycopg.errors.RaiseException as e:
        conn.rollback()
        print("2. Identidad inexistente:", str(e).splitlines()[0])

    # 3. Nombre vacío
    try:
        renombrar_ruta_proc(conn, "TP01", "   ")
    except psycopg.errors.RaiseException as e:
        conn.rollback()
        print("3. Nombre vacío:", str(e).splitlines()[0])
    print("   El nombre no cambió:", nombre_desde_otra_conexion("TP01"))

    # 4. Llamada dentro de una transacción que se revierte
    renombrar_ruta_proc(conn, "TP01", "Nombre provisional")
    print("4. Dentro de la transacción:      ", buscar_ruta(conn, "TP01").nombre)
    print("   Otra conexión, sin confirmar:  ", nombre_desde_otra_conexion("TP01"))
    conn.rollback()
    print("   Tras el rollback:              ", nombre_desde_otra_conexion("TP01"))

    # Limpieza
    eliminar_ruta(conn, "TP01")
    conn.commit()
finally:
    conn.close()