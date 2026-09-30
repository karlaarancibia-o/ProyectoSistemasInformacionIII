from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MovimientoStockCreate(BaseModel):
    lote_id: int
    tipo_movimiento: str = Field(..., pattern="^(entrada|salida)$")
    cantidad: int = Field(..., gt=0)
    usuario_id: int | None = None
    punto_id: int | None = None
    observacion: str | None = None
    fecha_movimiento: datetime | None = None


class MovimientoStockResponse(MovimientoStockCreate):
    id: int
    fecha_movimiento: datetime

    model_config = ConfigDict(from_attributes=True)
