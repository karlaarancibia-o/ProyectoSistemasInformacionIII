from dataclasses import dataclass
from datetime import date

from app.domain.exceptions import DatosInvalidosError


@dataclass
class RegistroVacunacion:
    """Una dosis efectivamente aplicada a un paciente (evento 8)."""

    paciente_id: int
    campana_id: int
    punto_id: int
    lote_id: int
    vacuna_id: int
    fecha_aplicacion: date
    numero_dosis: int
    es_refuerzo: bool = False
    id: int | None = None

    def __post_init__(self):
        if self.numero_dosis <= 0:
            raise DatosInvalidosError("El número de dosis debe ser positivo")
        if self.fecha_aplicacion > date.today():
            raise DatosInvalidosError("La fecha de aplicación no puede ser futura")
