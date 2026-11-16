from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Ruta(Base):
    __tablename__ = "ruta"
    __table_args__ = (
        CheckConstraint("distancia_km > 0", name="ck_ruta_distancia_positiva"),
        CheckConstraint("desnivel_m IS NULL OR desnivel_m >= 0", name="ck_ruta_desnivel_no_negativo"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_ruta: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    distancia_km: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    desnivel_m: Mapped[int | None] = mapped_column(nullable=True)
    valle: Mapped[str] = mapped_column(String(80), nullable=False)
    dificultad: Mapped[str] = mapped_column(String(30), nullable=False)

    planes: Mapped[list["PlanViaje"]] = relationship(
        back_populates="ruta",
        passive_deletes=True,
    )


class PlanViaje(Base):
    __tablename__ = "plan_viaje"
    __table_args__ = (
        CheckConstraint("fecha_fin >= fecha_inicio", name="ck_plan_viaje_fecha_fin_no_anterior"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_plan: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    ruta_id: Mapped[int] = mapped_column(
        ForeignKey("ruta.id", ondelete="RESTRICT"),
        nullable=False,
    )
    fecha_inicio: Mapped[date] = mapped_column(nullable=False)
    fecha_fin: Mapped[date] = mapped_column(nullable=False)
    estado: Mapped[str] = mapped_column(String(30), nullable=False)

    ruta: Mapped[Ruta] = relationship(back_populates="planes", passive_deletes=True)
