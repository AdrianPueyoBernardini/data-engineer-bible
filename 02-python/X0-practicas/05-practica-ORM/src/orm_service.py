from __future__ import annotations

from datetime import date

from sqlalchemy import select, text

from src.db import SessionLocal
from src.models import PlanViaje, Ruta


def crear_ruta(
    *,
    id_ruta: str,
    nombre: str,
    distancia_km: float,
    desnivel_m: int | None,
    valle: str,
    dificultad: str,
) -> Ruta:
    """Crea una ruta y la confirma en la base."""
    ruta = Ruta(
        id_ruta=id_ruta,
        nombre=nombre,
        distancia_km=distancia_km,
        desnivel_m=desnivel_m,
        valle=valle,
        dificultad=dificultad,
    )
    with SessionLocal() as session:
        session.add(ruta)
        session.commit()
    return ruta


def buscar_ruta_por_id_externo(id_ruta: str) -> Ruta | None:
    """Busca una ruta por su identidad externa; devuelve None si no existe."""
    with SessionLocal() as session:
        return session.scalar(select(Ruta).where(Ruta.id_ruta == id_ruta))


def actualizar_ruta(id_ruta: str, **campos) -> Ruta:
    """Modifica una ruta existente y la vuelve a leer en nueva Session."""
    with SessionLocal() as session:
        ruta = session.scalar(select(Ruta).where(Ruta.id_ruta == id_ruta))
        if ruta is None:
            raise ValueError(f"No existe la ruta {id_ruta}")
        for nombre, valor in campos.items():
            setattr(ruta, nombre, valor)
        session.commit()
        return ruta


def borrar_ruta(id_ruta: str) -> bool:
    """Borra una ruta si no tiene planes asociados; si no, PostgreSQL lanza IntegrityError."""
    with SessionLocal() as session:
        ruta = session.scalar(select(Ruta).where(Ruta.id_ruta == id_ruta))
        if ruta is None:
            return False
        session.delete(ruta)
        session.commit()
        return True


def crear_plan(
    *,
    id_plan: str,
    id_ruta: str,
    fecha_inicio: date,
    fecha_fin: date,
    estado: str,
) -> PlanViaje:
    """Crea un plan asociado a una ruta existente."""
    with SessionLocal() as session:
        ruta = session.scalar(select(Ruta).where(Ruta.id_ruta == id_ruta))
        if ruta is None:
            raise ValueError(f"La ruta {id_ruta} no existe")
        plan = PlanViaje(
            id_plan=id_plan,
            ruta_id=ruta.id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            estado=estado,
        )
        session.add(plan)
        session.commit()
        return plan


def buscar_plan_por_id_externo(id_plan: str) -> PlanViaje | None:
    """Busca un plan por su identidad externa."""
    with SessionLocal() as session:
        return session.scalar(select(PlanViaje).where(PlanViaje.id_plan == id_plan))


def borrar_plan(id_plan: str) -> bool:
    """Borra un plan por su identidad externa."""
    with SessionLocal() as session:
        plan = session.scalar(select(PlanViaje).where(PlanViaje.id_plan == id_plan))
        if plan is None:
            return False
        session.delete(plan)
        session.commit()
        return True


def crear_ruta_y_plan_en_transaccion(
    *,
    id_ruta: str,
    nombre: str,
    distancia_km: float,
    desnivel_m: int | None,
    valle: str,
    dificultad: str,
    id_plan: str,
    fecha_inicio: date,
    fecha_fin: date,
    estado: str,
    forzar_error: bool = False,
) -> tuple[Ruta, PlanViaje]:
    """Demuestra una transacción con dos cambios: si algo falla, se hace rollback."""
    with SessionLocal() as session:
        try:
            ruta = Ruta(
                id_ruta=id_ruta,
                nombre=nombre,
                distancia_km=distancia_km,
                desnivel_m=desnivel_m,
                valle=valle,
                dificultad=dificultad,
            )
            session.add(ruta)
            session.flush()

            plan = PlanViaje(
                id_plan=id_plan,
                ruta_id=ruta.id,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                estado=estado,
            )
            session.add(plan)
            session.flush()

            if forzar_error:
                raise RuntimeError("fallo forzado")

            session.commit()
            return ruta, plan
        except Exception:
            session.rollback()
            raise


def buscar_ruta_por_sql(id_ruta: str) -> dict | None:
    """Consulta directa con SQL parametrizado para comparar el resultado con la ORM."""
    with SessionLocal() as session:
        row = session.execute(
            text(
                """
                SELECT id, id_ruta, nombre, distancia_km, desnivel_m, valle, dificultad
                FROM ruta
                WHERE id_ruta = :id_ruta
                """
            ),
            {"id_ruta": id_ruta},
        ).mappings().first()
        return dict(row) if row is not None else None
