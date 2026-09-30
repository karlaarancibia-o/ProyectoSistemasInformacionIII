from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class RegistrarEntradaDosisRequest(BaseModel):
    vacuna_id: int
    numero_lote: str = Field(..., min_length=1, max_length=50)
    fecha_fabricacion: date
    fecha_vencimiento: date
    cantidad_inicial: int = Field(..., gt=0, description="Dosis que ingresan")
    umbral_minimo: int = Field(..., ge=0)
    # La entrada SIEMPRE ingresa al almacén central; por eso no lleva punto_id.


class RegistrarSalidaDosisRequest(BaseModel):
    lote_id: int = Field(..., description="Lote del almacén central que se despacha")
    punto_id: int = Field(..., description="Punto de vacunación de destino")
    cantidad: int = Field(..., gt=0)


class LoteDosisResponse(BaseModel):
    id: int
    vacuna_id: int
    numero_lote: str
    fecha_fabricacion: date
    fecha_vencimiento: date
    cantidad_inicial: int
    cantidad_actual: int
    umbral_minimo: int
    punto_id: int | None = None
    stock_bajo: bool

    model_config = ConfigDict(from_attributes=True)


class RegistrarTemperaturaRequest(BaseModel):
    vacuna_id: int
    temperatura_celsius: float
    fecha_hora: datetime
    usuario_id: int | None = None
    observacion: str | None = None


class RegistroTemperaturaResponse(BaseModel):
    id: int
    punto_id: int
    vacuna_id: int
    usuario_id: int | None = None
    temperatura_celsius: float
    fecha_hora: datetime
    observacion: str | None = None
    fuera_de_rango: bool

    model_config = ConfigDict(from_attributes=True)


class ResultadoRevisionInventarioResponse(BaseModel):
    lotes_con_stock_bajo: list[LoteDosisResponse]
    lotes_vencidos: list[LoteDosisResponse]
