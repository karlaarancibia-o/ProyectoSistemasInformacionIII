from pydantic import BaseModel, ConfigDict, Field


class EsquemaVacunacionCreate(BaseModel):
    vacuna_id: int
    grupo_edad_id: int
    cantidad_dosis: int = Field(..., gt=0)
    dias_entre_dosis: int = Field(..., ge=0)
    requiere_refuerzo: bool = False
    meses_refuerzo: int | None = Field(default=None, ge=0)


class EsquemaVacunacionUpdate(EsquemaVacunacionCreate):
    pass


class EsquemaVacunacionResponse(EsquemaVacunacionCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
