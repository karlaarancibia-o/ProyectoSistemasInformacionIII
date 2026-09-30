from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class RegistrarDosisAplicadaRequest(BaseModel):
    paciente_id: int
    campana_id: int
    punto_id: int
    lote_id: int
    fecha_aplicacion: date
    numero_dosis: int | None = Field(
        default=None,
        gt=0,
        description="Opcional: el sistema lo calcula según el esquema. Si se envía, debe coincidir.",
    )
    es_refuerzo: bool | None = Field(
        default=None,
        description="Opcional: el sistema lo calcula según el esquema. Si se envía, debe coincidir.",
    )


class RegistroVacunacionResponse(BaseModel):
    id: int
    paciente_id: int
    campana_id: int
    punto_id: int
    lote_id: int
    vacuna_id: int
    fecha_aplicacion: date
    numero_dosis: int
    es_refuerzo: bool

    model_config = ConfigDict(from_attributes=True)


class EsquemaVacunacionResponse(BaseModel):
    paciente_id: int
    vacuna_id: int
    dosis_aplicadas: int
    dosis_requeridas: int
    dosis_pendientes: int
    tiene_refuerzo_pendiente: bool
    esquema_completo: bool
    grupo_edad_id: int | None = None
    refuerzos_aplicados: int = 0
    proxima_dosis_numero: int | None = None
    proxima_dosis_es_refuerzo: bool | None = None
    fecha_minima_proxima_dosis: date | None = None

    model_config = ConfigDict(from_attributes=True)


class PacienteConEsquemaResponse(BaseModel):
    paciente_id: int
    esquema: EsquemaVacunacionResponse
