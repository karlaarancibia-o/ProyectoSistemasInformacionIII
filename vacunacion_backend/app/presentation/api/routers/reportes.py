from fastapi import APIRouter, Depends
from app.presentation.api.dependencias import requiere_administrador

from app.application.use_cases.reportes.generar_reporte_cobertura import (
    GenerarReporteCobertura,
)
from app.domain.repositories.campana_repository import CampanaRepository
from app.domain.repositories.grupo_edad_repository import GrupoEdadRepository
from app.domain.repositories.paciente_repository import PacienteRepository
from app.domain.repositories.registro_vacunacion_repository import (
    RegistroVacunacionRepository,
)
from app.presentation.api.dependencias import (
    get_campana_repository,
    get_grupo_edad_repository,
    get_paciente_repository,
    get_registro_vacunacion_repository,
    obtener_usuario_actual,
)
from app.presentation.api.schemas.reporte import ReporteCoberturaResponse

router = APIRouter(prefix="/reportes", tags=["Reportes y Seguimiento"], dependencies=[Depends(obtener_usuario_actual)])


@router.get("/cobertura/{campana_id}", response_model=ReporteCoberturaResponse, dependencies=[Depends(requiere_administrador)])
def generar_reporte_cobertura(
    campana_id: int,
    campana_repo: CampanaRepository = Depends(get_campana_repository),
    paciente_repo: PacienteRepository = Depends(get_paciente_repository),
    registro_repo: RegistroVacunacionRepository = Depends(
        get_registro_vacunacion_repository
    ),
    grupo_repo: GrupoEdadRepository = Depends(get_grupo_edad_repository),
):
    """Evento 28: el administrador consulta el reporte de cobertura de vacunación."""
    caso_de_uso = GenerarReporteCobertura(campana_repo, paciente_repo, registro_repo, grupo_repo)
    return caso_de_uso.ejecutar(campana_id)
