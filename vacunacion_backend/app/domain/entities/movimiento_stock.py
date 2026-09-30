from dataclasses import dataclass
from datetime import datetime

from app.domain.exceptions import DatosInvalidosError

TIPOS_MOVIMIENTO = ("entrada", "salida")


@dataclass
class MovimientoStock:
    """Registro de auditoría de una entrada o salida de dosis de un lote."""

    lote_id: int
    tipo_movimiento: str
    cantidad: int
    fecha_movimiento: datetime
    usuario_id: int | None = None
    punto_id: int | None = None
    observacion: str | None = None
    id: int | None = None

    def __post_init__(self):
        if self.tipo_movimiento not in TIPOS_MOVIMIENTO:
            raise DatosInvalidosError(
                "El tipo de movimiento debe ser 'entrada' o 'salida'"
            )
        if self.cantidad <= 0:
            raise DatosInvalidosError("La cantidad del movimiento debe ser positiva")
