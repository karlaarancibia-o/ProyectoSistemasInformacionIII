from dataclasses import dataclass
from datetime import date

from app.domain.exceptions import DatosInvalidosError


@dataclass
class AntecedenteVacunacion:
    paciente_id: int
    vacuna: str
    fecha_aplicacion: date
    numero_dosis: int
    id: int | None = None
    observaciones: str | None = None

    def __post_init__(self):
        if not self.vacuna.strip():
            raise DatosInvalidosError("La vacuna del antecedente es obligatoria")
        if self.numero_dosis <= 0:
            raise DatosInvalidosError("El número de dosis debe ser positivo")
        if self.fecha_aplicacion > date.today():
            raise DatosInvalidosError("La fecha del antecedente no puede ser futura")
