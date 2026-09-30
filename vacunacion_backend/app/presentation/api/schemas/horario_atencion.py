from datetime import time

from pydantic import BaseModel, ConfigDict, Field


class HorarioAtencionCreate(BaseModel):
    dia_semana: int = Field(..., ge=0, le=6, description="0=lunes .. 6=domingo")
    hora_apertura: time
    hora_cierre: time


class HorarioAtencionResponse(HorarioAtencionCreate):
    id: int
    punto_id: int

    model_config = ConfigDict(from_attributes=True)
