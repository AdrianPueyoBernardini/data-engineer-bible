from dataclasses import dataclass
from typing import Optional


@dataclass
class Ruta:
    id_ruta: str
    nombre: str
    distancia_km: float
    desnivel_m: Optional[int]   # None si no hay dato
    valle: str
    dificultad: str


SELECT_RUTA = (
    "SELECT id_ruta, nombre, distancia_km, desnivel_m, valle, dificultad "
    "FROM ruta"
)

# Opción permitida -> trozo de SQL conocido. Un identificador no puede ir como parámetro.
ORDENES = {
    "nombre": "ORDER BY nombre, id_ruta",
    "distancia": "ORDER BY distancia_km, id_ruta",
    "desnivel": "ORDER BY desnivel_m NULLS LAST, id_ruta",
}


def fila_a_ruta(fila):
    return Ruta(
        id_ruta=fila[0],
        nombre=fila[1],
        distancia_km=float(fila[2]),
        desnivel_m=fila[3],
        valle=fila[4],
        dificultad=fila[5],
    )


def validar_ruta(r):
    if not r.id_ruta or not r.id_ruta.strip():
        raise ValueError("id_ruta es obligatorio")
    if not r.nombre or not r.nombre.strip():
        raise ValueError("nombre es obligatorio")
    if r.distancia_km is None or r.distancia_km <= 0:
        raise ValueError("distancia_km debe ser mayor que 0")
    if r.desnivel_m is not None and r.desnivel_m < 0:
        raise ValueError("desnivel_m no puede ser negativo")
    if not r.valle or not r.valle.strip():
        raise ValueError("valle es obligatorio")
    if not r.dificultad or not r.dificultad.strip():
        raise ValueError("dificultad es obligatoria")


def crear_ruta(conn, ruta):
    validar_ruta(ruta)
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO ruta (id_ruta, nombre, distancia_km, desnivel_m, valle, dificultad) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (ruta.id_ruta, ruta.nombre, ruta.distancia_km,
             ruta.desnivel_m, ruta.valle, ruta.dificultad),
        )


def buscar_ruta(conn, id_ruta):
    with conn.cursor() as cur:
        cur.execute(SELECT_RUTA + " WHERE id_ruta = %s", (id_ruta,))
        fila = cur.fetchone()
    return fila_a_ruta(fila) if fila else None


def listar_rutas(conn, valle=None, dificultad=None, orden="nombre"):
    if orden not in ORDENES:
        raise ValueError(f"Orden no permitido: {orden}. Opciones: {list(ORDENES)}")
    condiciones = []
    params = []
    if valle is not None:
        condiciones.append("valle = %s")
        params.append(valle)
    if dificultad is not None:
        condiciones.append("dificultad = %s")
        params.append(dificultad)

    sql = SELECT_RUTA
    if condiciones:
        sql += " WHERE " + " AND ".join(condiciones)
    sql += " " + ORDENES[orden]

    with conn.cursor() as cur:
        cur.execute(sql, params)
        filas = cur.fetchall()
    return [fila_a_ruta(f) for f in filas]


def modificar_ruta(conn, ruta):
    validar_ruta(ruta)
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE ruta SET nombre = %s, distancia_km = %s, desnivel_m = %s, "
            "valle = %s, dificultad = %s WHERE id_ruta = %s",
            (ruta.nombre, ruta.distancia_km, ruta.desnivel_m,
             ruta.valle, ruta.dificultad, ruta.id_ruta),
        )
        return cur.rowcount


def eliminar_ruta(conn, id_ruta):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM ruta WHERE id_ruta = %s", (id_ruta,))
        return cur.rowcount

def renombrar_ruta_proc(conn, id_ruta, nuevo_nombre):
    """Invoca el procedimiento almacenado. No confirma: decide quien llama."""
    with conn.cursor() as cur:
        cur.execute("CALL renombrar_ruta(%s, %s)", (id_ruta, nuevo_nombre))