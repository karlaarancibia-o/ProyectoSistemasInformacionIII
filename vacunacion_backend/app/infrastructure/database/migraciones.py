"""Ajustes mínimos de esquema para bases ya creadas.

`Base.metadata.create_all` crea tablas nuevas pero NO modifica las existentes.
Si la BD se creó cuando `punto_id` era obligatorio en lotes/movimientos, el
almacén central (punto_id = NULL) fallaría. Aquí se deja la columna opcional.
"""
from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine

_COLUMNAS_OPCIONALES = (("lotes_dosis", "punto_id"), ("movimientos_stock", "punto_id"))


def permitir_almacen_central(engine: Engine) -> None:
    if engine.dialect.name != "postgresql":
        return
    inspector = inspect(engine)
    for tabla, columna in _COLUMNAS_OPCIONALES:
        if not inspector.has_table(tabla):
            continue
        info = next((c for c in inspector.get_columns(tabla) if c["name"] == columna), None)
        if info is None or info.get("nullable", True):
            continue
        with engine.begin() as conn:
            conn.execute(text(f'ALTER TABLE "{tabla}" ALTER COLUMN "{columna}" DROP NOT NULL'))
