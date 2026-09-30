from fastapi import APIRouter, Depends
from app.presentation.api.dependencias import requiere_administrador

from app.application.use_cases.esquema_vacunacion.actualizar_esquema_vacunacion import ActualizarEsquemaVacunacion
from app.application.use_cases.esquema_vacunacion.crear_esquema_vacunacion import CrearEsquemaVacunacion
from app.application.use_cases.esquema_vacunacion.eliminar_esquema_vacunacion import EliminarEsquemaVacunacion
from app.application.use_cases.esquema_vacunacion.listar_esquemas_vacunacion import ListarEsquemasVacunacion
from app.application.use_cases.esquema_vacunacion.obtener_esquema_vacunacion import ObtenerEsquemaVacunacion
from app.domain.repositories.esquema_vacunacion_repository import EsquemaVacunacionRepository
from app.domain.repositories.grupo_edad_repository import GrupoEdadRepository
from app.domain.repositories.vacuna_repository import VacunaRepository
from app.presentation.api.dependencias import (
    get_esquema_vacunacion_repository,
    get_grupo_edad_repository,
    get_vacuna_repository,
    obtener_usuario_actual,
)
from app.presentation.api.schemas.esquema_vacunacion import EsquemaVacunacionCreate, EsquemaVacunacionResponse, EsquemaVacunacionUpdate

router = APIRouter(prefix="/esquemas-vacunacion", tags=["Esquemas de Vacunación"], dependencies=[Depends(obtener_usuario_actual)])


@router.post("/", response_model=EsquemaVacunacionResponse, status_code=201, dependencies=[Depends(requiere_administrador)])
def crear(
    datos: EsquemaVacunacionCreate,
    repo: EsquemaVacunacionRepository = Depends(get_esquema_vacunacion_repository),
    vacuna_repo: VacunaRepository = Depends(get_vacuna_repository),
    grupo_edad_repo: GrupoEdadRepository = Depends(get_grupo_edad_repository),
):
    return CrearEsquemaVacunacion(repo, vacuna_repo, grupo_edad_repo).ejecutar(**datos.model_dump())


@router.get("/", response_model=list[EsquemaVacunacionResponse])
def listar(repo: EsquemaVacunacionRepository = Depends(get_esquema_vacunacion_repository)):
    return ListarEsquemasVacunacion(repo).ejecutar()


@router.get("/{esquema_id}", response_model=EsquemaVacunacionResponse)
def obtener(esquema_id: int, repo: EsquemaVacunacionRepository = Depends(get_esquema_vacunacion_repository)):
    return ObtenerEsquemaVacunacion(repo).ejecutar(esquema_id)


@router.put("/{esquema_id}", response_model=EsquemaVacunacionResponse, dependencies=[Depends(requiere_administrador)])
def actualizar(
    esquema_id: int,
    datos: EsquemaVacunacionUpdate,
    repo: EsquemaVacunacionRepository = Depends(get_esquema_vacunacion_repository),
    vacuna_repo: VacunaRepository = Depends(get_vacuna_repository),
    grupo_edad_repo: GrupoEdadRepository = Depends(get_grupo_edad_repository),
):
    return ActualizarEsquemaVacunacion(repo, vacuna_repo, grupo_edad_repo).ejecutar(esquema_id, **datos.model_dump())


@router.delete("/{esquema_id}", status_code=204, dependencies=[Depends(requiere_administrador)])
def eliminar(esquema_id: int, repo: EsquemaVacunacionRepository = Depends(get_esquema_vacunacion_repository)):
    EliminarEsquemaVacunacion(repo).ejecutar(esquema_id)
