from pydantic import BaseModel, ConfigDict, Field


class GrupoEdadBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    edad_min: int = Field(..., ge=0)
    edad_max: int = Field(..., ge=0)
    prioridad: int = Field(..., gt=0, description="1 = máxima prioridad")
    descripcion: str | None = None


class GrupoEdadCreate(GrupoEdadBase):
    pass


class GrupoEdadUpdate(GrupoEdadBase):
    pass


class EditarPrioridadRequest(BaseModel):
    nueva_prioridad: int = Field(..., gt=0)


class GrupoEdadResponse(GrupoEdadBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
