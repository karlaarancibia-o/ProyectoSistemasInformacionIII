"""Tablas de asociación many-to-many.

Viven aparte porque las usan modelos de ambos lados (ej. campana.py y
punto_vacunacion.py importan campana_punto_vacunacion).
"""

from sqlalchemy import Column, ForeignKey, Integer, Table

from app.infrastructure.database.connection import Base

campana_grupo_edad = Table(
    "campana_grupo_edad",
    Base.metadata,
    Column("campana_id", Integer, ForeignKey("campanas.id"), primary_key=True),
    Column("grupo_edad_id", Integer, ForeignKey("grupos_edad.id"), primary_key=True),
)

campana_punto_vacunacion = Table(
    "campana_punto_vacunacion",
    Base.metadata,
    Column("campana_id", Integer, ForeignKey("campanas.id"), primary_key=True),
    Column("punto_id", Integer, ForeignKey("puntos_vacunacion.id"), primary_key=True),
)

vacuna_grupo_edad = Table(
    "vacuna_grupo_edad",
    Base.metadata,
    Column("vacuna_id", Integer, ForeignKey("vacunas.id"), primary_key=True),
    Column("grupo_edad_id", Integer, ForeignKey("grupos_edad.id"), primary_key=True),
)
