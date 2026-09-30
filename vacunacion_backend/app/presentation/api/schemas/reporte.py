from pydantic import BaseModel, ConfigDict


class ReporteCoberturaResponse(BaseModel):
    campana_id: int
    nombre_campana: str
    total_pacientes_registrados: int
    total_dosis_aplicadas: int
    pacientes_vacunados: int
    porcentaje_cobertura: float
    total_pacientes_objetivo: int = 0

    model_config = ConfigDict(from_attributes=True)
