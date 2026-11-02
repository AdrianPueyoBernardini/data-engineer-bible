from dataclasses import replace

from db import abrir_conexion
from repositorio import buscar_ruta
from importador import (
    leer_rutas_csv, leer_planes_json, importar_rutas, importar_planes,
)


def mostrar(titulo, res):
    print(f"{titulo}: nuevos={len(res.nuevos)} duplicados={len(res.duplicados)} "
          f"conflictos={len(res.conflictos)} rechazados={len(res.rechazados)}")
    for clave, motivo in res.conflictos + res.rechazados:
        print("    -", clave, "->", motivo)


conn = abrir_conexion()
try:
    rutas, rech_rutas = leer_rutas_csv()
    planes, rech_planes = leer_planes_json()
    print(f"Leídas: {len(rutas)} rutas válidas, {len(planes)} planes válidos\n")

    mostrar("1ª importación de rutas", importar_rutas(conn, rutas, rech_rutas))
    _, res = importar_planes(conn, planes, rech_planes)
    mostrar("1ª importación de planes", res)

    print()
    mostrar("2ª importación de rutas", importar_rutas(conn, rutas, rech_rutas))
    _, res = importar_planes(conn, planes, rech_planes)
    mostrar("2ª importación de planes", res)

    print()
    alterada = replace(rutas[0], nombre=rutas[0].nombre + " (modificada)")
    mostrar("Conflicto provocado", importar_rutas(conn, [alterada]))
    print("En la base sigue:", buscar_ruta(conn, rutas[0].id_ruta))
finally:
    conn.close()