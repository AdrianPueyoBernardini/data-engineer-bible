from dataclasses import dataclass
from datetime import date

# Ajusta estos valores a los estados que uses en tu planes.json de P1
ESTADOS_VALIDOS = ("planificado", "pendiente", "confirmado", "cancelado", "realizado")


@dataclass
class Plan:
    id_plan: str
    id_ruta: str          # código externo de la ruta, no el id interno
    fecha_inicio: date
    fecha_fin: date
    estado: str


SELECT_PLAN = (
    "SELECT p.id_plan, r.id_ruta, p.fecha_inicio, p.fecha_fin, p.estado "
    "FROM plan_viaje p JOIN ruta r ON r.id = p.ruta_id"
)

ORDENES_PLAN = {
    "fecha": "ORDER BY p.fecha_inicio, p.id_plan",
    "estado": "ORDER BY p.estado, p.fecha_inicio, p.id_plan",
}


def fila_a_plan(fila):
    return Plan(
        id_plan=fila[0],
        id_ruta=fila[1],
        fecha_inicio=fila[2],
        fecha_fin=fila[3],
        estado=fila[4],
    )


def validar_plan(p):
    if not p.id_plan or not p.id_plan.strip():
        raise ValueError("id_plan es obligatorio")
    if not p.id_ruta or not p.id_ruta.strip():
        raise ValueError("id_ruta es obligatorio")
    if not isinstance(p.fecha_inicio, date) or not isinstance(p.fecha_fin, date):
        raise ValueError("Las fechas deben ser de tipo date")
    if p.fecha_fin < p.fecha_inicio:
        raise ValueError("fecha_fin no puede ser anterior a fecha_inicio")
    if p.estado not in ESTADOS_VALIDOS:
        raise ValueError(f"Estado no válido: {p.estado}. Opciones: {ESTADOS_VALIDOS}")


def crear_plan(conn, plan):
    validar_plan(plan)
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO plan_viaje (id_plan, ruta_id, fecha_inicio, fecha_fin, estado) "
            "SELECT %s, id, %s, %s, %s FROM ruta WHERE id_ruta = %s",
            (plan.id_plan, plan.fecha_inicio, plan.fecha_fin, plan.estado, plan.id_ruta),
        )
        if cur.rowcount == 0:
            raise ValueError(f"La ruta {plan.id_ruta} no existe")


def buscar_plan(conn, id_plan):
    with conn.cursor() as cur:
        cur.execute(SELECT_PLAN + " WHERE p.id_plan = %s", (id_plan,))
        fila = cur.fetchone()
    return fila_a_plan(fila) if fila else None


def listar_planes(conn, estado=None, id_ruta=None, desde=None, orden="fecha"):
    if orden not in ORDENES_PLAN:
        raise ValueError(f"Orden no permitido: {orden}. Opciones: {list(ORDENES_PLAN)}")
    condiciones = []
    params = []
    if estado is not None:
        condiciones.append("p.estado = %s")
        params.append(estado)
    if id_ruta is not None:
        condiciones.append("r.id_ruta = %s")
        params.append(id_ruta)
    if desde is not None:
        condiciones.append("p.fecha_inicio >= %s")
        params.append(desde)

    sql = SELECT_PLAN
    if condiciones:
        sql += " WHERE " + " AND ".join(condiciones)
    sql += " " + ORDENES_PLAN[orden]

    with conn.cursor() as cur:
        cur.execute(sql, params)
        filas = cur.fetchall()
    return [fila_a_plan(f) for f in filas]


def modificar_plan(conn, plan):
    validar_plan(plan)
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE plan_viaje SET fecha_inicio = %s, fecha_fin = %s, estado = %s "
            "WHERE id_plan = %s",
            (plan.fecha_inicio, plan.fecha_fin, plan.estado, plan.id_plan),
        )
        return cur.rowcount


def eliminar_plan(conn, id_plan):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM plan_viaje WHERE id_plan = %s", (id_plan,))
        return cur.rowcount


def planes_con_ruta(conn, valle=None):
    """Consulta que relaciona B con A: cada plan con datos de su ruta."""
    sql = (
        "SELECT p.id_plan, p.fecha_inicio, p.estado, r.nombre, r.valle "
        "FROM plan_viaje p JOIN ruta r ON r.id = p.ruta_id"
    )
    params = []
    if valle is not None:
        sql += " WHERE r.valle = %s"
        params.append(valle)
    sql += " ORDER BY p.fecha_inicio, p.id_plan"
    with conn.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def contar_planes_por_ruta(conn):
    """Recuento de planes por ruta, incluidas las rutas sin ningún plan."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT r.id_ruta, r.nombre, COUNT(p.id) AS num_planes "
            "FROM ruta r LEFT JOIN plan_viaje p ON p.ruta_id = r.id "
            "GROUP BY r.id, r.id_ruta, r.nombre "
            "ORDER BY num_planes DESC, r.id_ruta"
        )
        return cur.fetchall()