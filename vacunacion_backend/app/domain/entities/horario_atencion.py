from dataclasses import dataclass
from datetime import time

from app.domain.exceptions import DatosInvalidosError

DIAS_SEMANA = range(0, 7)  # 0 = lunes ... 6 = domingo


@dataclass
class HorarioAtencion:
    punto_id: int
    dia_semana: int
    hora_apertura: time
    hora_cierre: time
    id: int | None = None

    def __post_init__(self):
        if self.dia_semana not in DIAS_SEMANA:
            raise DatosInvalidosError("Día de la semana inválido (0=lunes .. 6=domingo)")
        if self.hora_cierre <= self.hora_apertura:
            raise DatosInvalidosError(
                "La hora de cierre debe ser posterior a la hora de apertura"
            )
