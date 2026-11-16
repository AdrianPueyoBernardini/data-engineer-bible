from datetime import date

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.db import engine, SessionLocal
from src.models import PlanViaje, Ruta
from src.orm_service import (
    buscar_plan_por_id_externo,
    buscar_ruta_por_id_externo,
    borrar_plan,
    borrar_ruta,
    crear_plan,
    crear_ruta,
    actualizar_ruta,
)


@pytest.fixture(autouse=True)
def limpiar_bd():
    with SessionLocal() as session:
        session.execute(PlanViaje.__table__.delete())
        session.execute(Ruta.__table__.delete())
        session.commit()
    yield
    with SessionLocal() as session:
        session.execute(PlanViaje.__table__.delete())
        session.execute(Ruta.__table__.delete())
        session.commit()


def test_crud_ruta_y_relectura_en_nueva_session():
    ruta = crear_ruta(
        id_ruta="R-ALM-001",
        nombre="Ruta de prueba",
        distancia_km=12.5,
        desnivel_m=340,
        valle="Valle de prueba",
        dificultad="moderada",
    )
    assert ruta.id_ruta == "R-ALM-001"

    recuperada = buscar_ruta_por_id_externo("R-ALM-001")
    assert recuperada is not None
    assert recuperada.nombre == "Ruta de prueba"

    actualizar_ruta("R-ALM-001", nombre="Ruta modificada")
    relectura = buscar_ruta_por_id_externo("R-ALM-001")
    assert relectura is not None and relectura.nombre == "Ruta modificada"

    borrar_ruta("R-ALM-001")
    assert buscar_ruta_por_id_externo("R-ALM-001") is None


def test_relacion_y_join_entre_ruta_y_plan():
    ruta = crear_ruta(
        id_ruta="R-REL-001",
        nombre="Ruta con plan",
        distancia_km=8.4,
        desnivel_m=220,
        valle="Valle de prueba",
        dificultad="fácil",
    )
    crear_plan(
        id_plan="P-REL-001",
        id_ruta="R-REL-001",
        fecha_inicio=date(2026, 1, 10),
        fecha_fin=date(2026, 1, 12),
        estado="planificado",
    )

    with SessionLocal() as session:
        planes = session.execute(
            select(PlanViaje)
            .join(Ruta)
            .where(Ruta.id_ruta == "R-REL-001")
            .order_by(PlanViaje.fecha_inicio, PlanViaje.id_plan)
        ).scalars().all()
        assert len(planes) == 1
        assert planes[0].ruta.id_ruta == "R-REL-001"
        assert planes[0].ruta.nombre == "Ruta con plan"

    # Resultado vacío no debe lanzar error.
    with SessionLocal() as session:
        vacio = session.execute(
            select(PlanViaje).where(PlanViaje.id_plan == "NO-EXISTE")
        ).scalars().all()
        assert vacio == []


def test_borrado_con_restriccion_y_borrado_libre():
    ruta = crear_ruta(
        id_ruta="R-RESTR-001",
        nombre="Ruta protegida",
        distancia_km=9.0,
        desnivel_m=0,
        valle="Valle protegido",
        dificultad="moderada",
    )
    crear_plan(
        id_plan="P-RESTR-001",
        id_ruta="R-RESTR-001",
        fecha_inicio=date(2026, 2, 1),
        fecha_fin=date(2026, 2, 3),
        estado="confirmado",
    )

    with pytest.raises(IntegrityError):
        borrar_ruta("R-RESTR-001")

    nuevo = crear_ruta(
        id_ruta="R-LIBRE-001",
        nombre="Ruta libre",
        distancia_km=3.2,
        desnivel_m=None,
        valle="Valle libre",
        dificultad="fácil",
    )
    borrar_ruta("R-LIBRE-001")
    assert buscar_ruta_por_id_externo("R-LIBRE-001") is None


def test_crear_plan_y_desde_otra_session():
    ruta = crear_ruta(
        id_ruta="R-OTRA-001",
        nombre="Otra ruta",
        distancia_km=4.0,
        desnivel_m=50,
        valle="Valle otra",
        dificultad="fácil",
    )
    plan = crear_plan(
        id_plan="P-OTRA-001",
        id_ruta="R-OTRA-001",
        fecha_inicio=date(2026, 3, 5),
        fecha_fin=date(2026, 3, 6),
        estado="pendiente",
    )
    assert plan.id_plan == "P-OTRA-001"
    assert buscar_plan_por_id_externo("P-OTRA-001") is not None

    borrar_plan("P-OTRA-001")
    assert buscar_plan_por_id_externo("P-OTRA-001") is None
