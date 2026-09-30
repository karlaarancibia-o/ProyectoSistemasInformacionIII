"""Reglas puras de edad y grupos de edad (sin dependencias de infraestructura)."""

from datetime import date

from app.domain.entities.grupo_edad import GrupoEdad


def calcular_edad(fecha_nacimiento: date, en_fecha: date) -> int:
    """Edad cumplida (en años) que tenía una persona en `en_fecha`."""
    edad = en_fecha.year - fecha_nacimiento.year
    if (en_fecha.month, en_fecha.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1
    return edad


def grupos_para_edad(grupos: list[GrupoEdad], edad: int) -> list[GrupoEdad]:
    """Grupos cuyo rango incluye la edad, del más al menos prioritario."""
    return sorted(
        (g for g in grupos if g.contiene_edad(edad)),
        key=lambda g: (g.prioridad, g.id or 0),
    )
