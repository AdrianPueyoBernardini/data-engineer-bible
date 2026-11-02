import psycopg

from db import abrir_conexion
from repositorio import (
    Ruta, crear_ruta, buscar_ruta, listar_rutas, modificar_ruta, eliminar_ruta,
)

conn = abrir_conexion()
try:
    # 0. Estado conocido: borrar el registro de prueba si quedó de otra ejecución
    eliminar_ruta(conn, "T001")
    conn.commit()

    # 1. Alta con apóstrofo en el nombre
    nueva = Ruta("T001", "Pico d'Aneto", 12.5, None, "Benasque", "Dificil")
    crear_ruta(conn, nueva)
    conn.commit()
    print("1. Alta confirmada")

    # 2. Lectura desde OTRA conexión (prueba de persistencia real)
    otra = abrir_conexion()
    try:
        print("2. Leída desde otra conexión:", buscar_ruta(otra, "T001"))
    finally:
        otra.close()

    # 3. Búsqueda de una clave inexistente
    print("3. Inexistente:", buscar_ruta(conn, "NOEXISTE"))

    # 4. Listado filtrado y ordenado
    print("4. Rutas de Benasque:", listar_rutas(conn, valle="Benasque", orden="nombre"))
    print("4b. Filtro sin resultados:", listar_rutas(conn, valle="Valle inventado"))

    # 5. Modificación
    nueva.distancia_km = 13.0
    nueva.desnivel_m = 1400
    print("5. Filas modificadas:", modificar_ruta(conn, nueva))
    conn.commit()
    print("   Tras modificar:", buscar_ruta(conn, "T001"))

    # 6. Modificar una clave que no existe
    fantasma = Ruta("NOEXISTE", "X", 1.0, None, "X", "X")
    print("6. Filas modificadas (inexistente):", modificar_ruta(conn, fantasma))
    conn.commit()

    # 7. Clave repetida: la base lo rechaza
    try:
        crear_ruta(conn, nueva)
    except psycopg.errors.UniqueViolation as e:
        conn.rollback()   # imprescindible tras un error de la base
        print("7. Clave repetida rechazada:", str(e).splitlines()[0])

    # 8. Borrado del registro de prueba
    print("8. Filas borradas:", eliminar_ruta(conn, "T001"))
    conn.commit()
    print("   Borrado otra vez:", eliminar_ruta(conn, "T001"))
    conn.commit()
finally:
    conn.close()