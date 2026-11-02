import csv
import json
import uuid
from dataclasses import dataclass, field
from datetime import date

from db import ROOT
from repositorio import Ruta, validar_ruta, buscar_ruta, crear_ruta
from repositorio_planes import Plan, validar_plan, buscar_plan, crear_plan

RUTAS_CSV = ROOT / "data" / "rutas.csv"
PLANES_JSON = ROOT / "data" / "planes.json"
DELIMITADOR = ","
CODIFICACION = "utf-8-sig"
COLUMNAS_RUTAS = ("id_ruta", "ruta", "distancia_km", "desnivel_m", "valle", "dificultad")

@dataclass
class Resultado:
    nuevos: list = field(default_factory=list)
    duplicados: list = field(default_factory=list)
    conflictos: list = field(default_factory=list)   # (clave, motivo)
    rechazados: list = field(default_factory=list)   # (clave, motivo)


# ---------- Lectura y validación de los archivos ----------

def leer_rutas_csv(ruta_csv=RUTAS_CSV):
    validas, rechazados = [], []
    with open(ruta_csv, encoding=CODIFICACION, newline="") as f:
        lector = csv.DictReader(f, delimiter=DELIMITADOR)
        lector.fieldnames = [c.strip().lower() for c in (lector.fieldnames or [])]
        faltan = set(COLUMNAS_RUTAS) - set(lector.fieldnames)
        if faltan:
            raise ValueError(
                f"El CSV no tiene las columnas {sorted(faltan)}. "
                f"Columnas encontradas: {lector.fieldnames}"
            )
        for n, fila in enumerate(lector, start=2):
            clave = (fila.get("id_ruta") or "").strip() or f"fila {n}"
            try:
                texto_desnivel = (fila["desnivel_m"] or "").strip()
                desnivel = None if texto_desnivel in ("", "—", "-") else int(texto_desnivel)
                ruta = Ruta(
                    id_ruta=fila["id_ruta"].strip(),
                    nombre=fila["ruta"].strip(),
                    distancia_km=round(float(fila["distancia_km"].strip().replace(",", ".")), 2),
                    desnivel_m=desnivel,
                    valle=fila["valle"].strip(),
                    dificultad=fila["dificultad"].strip(),
                )
                validar_ruta(ruta)
                validas.append(ruta)
            except (ValueError, KeyError, AttributeError) as e:
                rechazados.append((clave, f"fila {n}: {e}"))
    return validas, rechazados


def leer_planes_json(ruta_json=PLANES_JSON):
    with open(ruta_json, encoding="utf-8") as f:
        datos = json.load(f)
    validos, rechazados = [], []
    for n, d in enumerate(datos, start=1):
        clave = str(d.get("id_plan", f"registro {n}"))
        try:
            plan = Plan(
                id_plan=str(d["id_plan"]).strip(),
                id_ruta=str(d["id_ruta"]).strip(),
                fecha_inicio=date.fromisoformat(d["fecha_inicio"]),
                fecha_fin=date.fromisoformat(d["fecha_fin"]),
                estado=str(d["estado"]).strip(),
            )
            validar_plan(plan)
            validos.append(plan)
        except (ValueError, KeyError, TypeError) as e:
            rechazados.append((clave, f"registro {n}: {e}"))
    return validos, rechazados


# ---------- Importación de rutas (A) ----------

def importar_rutas(conn, rutas, rechazados_lectura=()):
    res = Resultado(rechazados=list(rechazados_lectura))
    vistas = {}
    for r in rutas:
        previa = vistas.get(r.id_ruta) or buscar_ruta(conn, r.id_ruta)
        if previa is None:
            res.nuevos.append(r)
            vistas[r.id_ruta] = r
        elif previa == r:
            res.duplicados.append(r.id_ruta)
        else:
            res.conflictos.append(
                (r.id_ruta, "ya existe con contenido distinto; se conserva el anterior")
            )
    try:
        for r in res.nuevos:
            crear_ruta(conn, r)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    return res


# ---------- Importación de planes (B) con transacción ----------

def clasificar_planes(conn, planes, rechazados_lectura=()):
    res = Resultado(rechazados=list(rechazados_lectura))
    with conn.cursor() as cur:
        cur.execute("SELECT id_ruta FROM ruta")
        rutas_existentes = {fila[0] for fila in cur.fetchall()}
    vistos = {}
    for p in planes:
        if p.id_ruta not in rutas_existentes:
            res.rechazados.append((p.id_plan, f"la ruta {p.id_ruta} no existe"))
            continue
        previo = vistos.get(p.id_plan) or buscar_plan(conn, p.id_plan)
        if previo is None:
            res.nuevos.append(p)
            vistos[p.id_plan] = p
        elif previo == p:
            res.duplicados.append(p.id_plan)
        else:
            res.conflictos.append(
                (p.id_plan, "ya existe con contenido distinto; se conserva el anterior")
            )
    return res


def guardar_lote_planes(conn, res, id_operacion, fallo_prueba=False):
    try:
        for p in res.nuevos:
            crear_plan(conn, p)
        if fallo_prueba:
            raise RuntimeError("Fallo de prueba antes de confirmar")
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO resumen_importacion "
                "(id_operacion, nuevos, duplicados, conflictos, rechazados) "
                "VALUES (%s, %s, %s, %s, %s)",
                (id_operacion, len(res.nuevos), len(res.duplicados),
                 len(res.conflictos), len(res.rechazados)),
            )
        conn.commit()
    except Exception:
        conn.rollback()
        raise


def importar_planes(conn, planes, rechazados_lectura=(), fallo_prueba=False):
    id_operacion = uuid.uuid4().hex
    res = clasificar_planes(conn, planes, rechazados_lectura)
    guardar_lote_planes(conn, res, id_operacion, fallo_prueba)
    return id_operacion, res


def existe_operacion(conn, id_operacion):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT 1 FROM resumen_importacion WHERE id_operacion = %s",
            (id_operacion,),
        )
        return cur.fetchone() is not None