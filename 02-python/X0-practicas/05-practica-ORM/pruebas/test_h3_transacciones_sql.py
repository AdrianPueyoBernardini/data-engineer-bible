from datetime import date

import pytest
from sqlalchemy import text

from src.db import SessionLocal
from src.models import PlanViaje, Ruta
from src.orm_service import (
    buscar_ruta_por_sql,
    crear_ruta_y_plan_en_transaccion,
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


def test_transaccion_rollback_dos_cambios():
    with pytest.raises(RuntimeError, match="fallo forzado"):
        crear_ruta_y_plan_en_transaccion(
            id_ruta="R-ROLL-001",
            nombre="Ruta rollback",
            distancia_km=15.5,
            desnivel_m=180,
            valle="Valle rollback",
            dificultad="difícil",
            id_plan="P-ROLL-001",
            fecha_inicio=date(2026, 5, 1),
            fecha_fin=date(2026, 5, 2),
            estado="pendiente",
            forzar_error=True,
        )

    with SessionLocal() as session:
        ruta = session.execute(
            text("SELECT COUNT(*) FROM ruta WHERE id_ruta = :id_ruta"),
            {"id_ruta": "R-ROLL-001"},
        ).scalar_one()
        plan = session.execute(
            text("SELECT COUNT(*) FROM plan_viaje WHERE id_plan = :id_plan"),
            {"id_plan": "P-ROLL-001"},
        ).scalar_one()

    assert ruta == 0
    assert plan == 0


def test_sql_parametrizado_devuelve_el_mismo_registro_que_orm():
    with SessionLocal() as session:
        ruta = Ruta(
            id_ruta="R-SQL-001",
            nombre="Ruta SQL",
            distancia_km=19.0,
            desnivel_m=300,
            valle="Valle SQL",
            dificultad="moderada",
        )
        session.add(ruta)
        session.flush()
        session.add(
            PlanViaje(
                id_plan="P-SQL-001",
                ruta_id=ruta.id,
                fecha_inicio=date(2026, 6, 1),
                fecha_fin=date(2026, 6, 3),
                estado="confirmado",
            )
        )
        session.commit()

    raw = buscar_ruta_por_sql("R-SQL-001")
    assert raw is not None
    assert raw["nombre"] == "Ruta SQL"
    assert raw["valle"] == "Valle SQL"

    with SessionLocal() as session:
        orm = session.execute(
            __import__("sqlalchemy").select(Ruta).where(Ruta.id_ruta == "R-SQL-001")
        ).scalar_one()

    assert orm.nombre == raw["nombre"]
    assert orm.valle == raw["valle"]
