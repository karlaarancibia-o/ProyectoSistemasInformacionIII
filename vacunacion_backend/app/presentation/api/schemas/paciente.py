from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.presentation.api.schemas.registro_vacunacion import RegistroVacunacionResponse


class PacienteBase(BaseModel):
    nombres: str = Field(..., min_length=2, max_length=150)
    apellidos: str = Field(..., min_length=2, max_length=150)
    carnet_identidad: str = Field(..., min_length=2, max_length=30)
    fecha_nacimiento: date
    sexo: str = Field(..., pattern="^[MF]$")
    telefono: str | None = None
    direccion: str | None = None


class PacienteCreate(PacienteBase):
    grupo_edad_id: int | None = None


class PacienteResponse(PacienteBase):
    id: int
    grupo_edad_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


class AntecedenteVacunacionCreate(BaseModel):
    vacuna: str = Field(..., min_length=2, max_length=100)
    fecha_aplicacion: date
    numero_dosis: int = Field(..., gt=0)
    observaciones: str | None = None


class AntecedenteVacunacionResponse(AntecedenteVacunacionCreate):
    id: int
    paciente_id: int

    model_config = ConfigDict(from_attributes=True)


class HistorialPacienteResponse(BaseModel):
    antecedentes: list[AntecedenteVacunacionResponse]
    dosis_aplicadas_en_el_sistema: list[RegistroVacunacionResponse]
