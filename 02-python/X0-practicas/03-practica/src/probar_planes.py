from datetime import date

import psycopg

from db import abrir_conexion
from repositorio import Ruta, crear_ruta, eliminar_ruta
from repositorio_planes import (
    Plan, crear_plan, buscar_plan, listar_planes, modificar_plan,
    eliminar_plan, planes_con_ruta, contar_planes_por_ruta,
)

conn = abrir_conexion()
try:
    # 0. Estado conocido: primero los planes, luego las rutas (por la clave foránea)
    for p in ("PT01", "PT02", "PT03"):
        eliminar_plan(conn, p)
    for r in ("T001", "T002"):
        eliminar_ruta(conn, r)
    conn.commit()

    # 1. Dos rutas de prueba
    crear_ruta(conn, Ruta("T001", "Pico d'Aneto", 12.5, None, "Benasque", "Dificil"))
    crear_ruta(conn, Ruta("T002", "Ibon de Plan", 8.5, 650, "Chistau", "Media"))
    conn.commit()

    # 2. Tres planes
    crear_plan(conn, Plan("PT01", "T001", date(2027, 7, 1), date(2027, 7, 3), "pendiente"))
    crear_plan(conn, Plan("PT02", "T001", date(2027, 8, 10), date(2027, 8, 12), "confirmado"))
    crear_plan(conn, Plan("PT03", "T002", date(2027, 7, 15), date(2027, 7, 16), "pendiente"))
    conn.commit()
    print("2. Planes creados")

    # 3. Lectura desde otra conexión
    otra = abrir_conexion()
    try:
        print("3. Desde otra conexión:", buscar_plan(otra, "PT01"))
    finally:
        otra.close()
    print("3b. Inexistente:", buscar_plan(conn, "NOEXISTE"))

    # 4. Plan con una ruta que no existe
    try:
        crear_plan(conn, Plan("PX", "NOEXISTE", date(2027, 7, 1), date(2027, 7, 2), "pendiente"))
    except ValueError as e:
        print("4. Rechazado:", e)

    # 5. Fechas al revés (lo frena el programa antes de llegar a la base)
    try:
        crear_plan(conn, Plan("PX", "T001", date(2027, 7, 3), date(2027, 7, 1), "pendiente"))
    except ValueError as e:
        print("5. Rechazado:", e)

    # 6. Listados filtrados
    print("6. Pendientes por fecha:")
    for p in listar_planes(conn, estado="pendiente", orden="fecha"):
        print("   ", p)
    print("6b. Desde agosto:", listar_planes(conn, desde=date(2027, 8, 1)))
    print("6c. Sin resultados:", listar_planes(conn, estado="cancelado"))

    # 7. Modificación
    p1 = buscar_plan(conn, "PT01")
    p1.estado = "confirmado"
    print("7. Filas modificadas:", modificar_plan(conn, p1))
    conn.commit()
    p1.id_plan = "NOEXISTE"
    print("7b. Filas modificadas (inexistente):", modificar_plan(conn, p1))
    conn.commit()

    # 8. Consultas que relacionan planes y rutas
    print("8. Planes de Benasque:")
    for fila in planes_con_ruta(conn, valle="Benasque"):
        print("   ", fila)
    print("8b. Recuento de planes por ruta:")
    for fila in contar_planes_por_ruta(conn):
        print("   ", fila)

    # 9. Borrar una ruta que tiene planes: la base lo impide
    try:
        eliminar_ruta(conn, "T001")
    except psycopg.errors.ForeignKeyViolation as e:
        conn.rollback()
        print("9. Borrado rechazado:", str(e).splitlines()[0])

    # 10. Borrar primero los dependientes y después la ruta
    print("10. Planes borrados:", eliminar_plan(conn, "PT01") + eliminar_plan(conn, "PT02"))
    print("    Ruta borrada:", eliminar_ruta(conn, "T001"))
    conn.commit()

    # Limpieza final
    eliminar_plan(conn, "PT03")
    eliminar_ruta(conn, "T002")
    conn.commit()
finally:
    conn.close()