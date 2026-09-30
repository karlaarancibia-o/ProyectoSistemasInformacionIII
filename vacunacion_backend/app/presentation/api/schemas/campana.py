from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class CampanaCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=150)
    descripcion: str | None = None
    tipo_temporada: str = Field(..., min_length=2, max_length=100)
    fecha_inicio: date
    fecha_fin: date
    vacuna_id: int
    grupo_edad_ids: list[int] = []


class AsignarPuntoRequest(BaseModel):
    punto_id: int


class AsignarGrupoEdadRequest(BaseModel):
    grupo_edad_id: int


class CampanaResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str | None = None
    tipo_temporada: str
    fecha_inicio: date
    fecha_fin: date
    vacuna_id: int
    estado: str
    grupo_edad_ids: list[int] = []
    punto_ids: list[int] = []

    model_config = ConfigDict(from_attributes=True)
