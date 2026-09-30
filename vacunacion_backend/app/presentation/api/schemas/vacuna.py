from pydantic import BaseModel, ConfigDict, Field


class VacunaCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=150)
    fabricante: str = Field(..., min_length=2, max_length=150)
    tipo: str = Field(..., min_length=2, max_length=100)
    temperatura_minima: float
    temperatura_maxima: float
    descripcion: str | None = None
    grupo_edad_ids: list[int] = Field(
        ...,
        min_length=1,
        description="Ids de grupos de edad ya creados a los que está indicada la vacuna",
    )


class VacunaUpdate(VacunaCreate):
    estado: str = Field(default="activa", pattern="^(activa|inactiva)$")


class VacunaResponse(VacunaCreate):
    id: int
    estado: str
    # vacunas antiguas pueden no tener grupos aún: se devuelve lista vacía
    grupo_edad_ids: list[int] = []

    model_config = ConfigDict(from_attributes=True)
