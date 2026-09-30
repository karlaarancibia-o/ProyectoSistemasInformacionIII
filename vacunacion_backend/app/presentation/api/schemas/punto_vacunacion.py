from pydantic import BaseModel, ConfigDict, Field


class PuntoVacunacionBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=150)
    direccion: str = Field(..., min_length=2, max_length=250)
    telefono: str | None = None
    capacidad: int = Field(..., gt=0)
    estado: str = "activo"


class PuntoVacunacionCreate(PuntoVacunacionBase):
    pass


class PuntoVacunacionUpdate(PuntoVacunacionBase):
    pass


class PuntoVacunacionResponse(PuntoVacunacionBase):
    id: int
    campana_ids: list[int] = []

    model_config = ConfigDict(from_attributes=True)
