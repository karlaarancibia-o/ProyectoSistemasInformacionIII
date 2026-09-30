from dataclasses import dataclass
from datetime import datetime

from app.domain.exceptions import DatosInvalidosError

RANGO_MIN_C = 2.0
RANGO_MAX_C = 8.0


@dataclass
class RegistroTemperatura:
    punto_id: int
    vacuna_id: int
    temperatura_celsius: float
    fecha_hora: datetime
    id: int | None = None
    usuario_id: int | None = None
    observacion: str | None = None
    # rango permitido de la vacuna almacenada; si no se informa, se usa el
    # rango general de cadena de frío (2–8 °C)
    rango_minimo: float | None = None
    rango_maximo: float | None = None

    def __post_init__(self):
        if self.fecha_hora > datetime.now():
            raise DatosInvalidosError("La fecha/hora del registro no puede ser futura")

    @property
    def fuera_de_rango(self) -> bool:
        minimo = RANGO_MIN_C if self.rango_minimo is None else self.rango_minimo
        maximo = RANGO_MAX_C if self.rango_maximo is None else self.rango_maximo
        return not (minimo <= self.temperatura_celsius <= maximo)
