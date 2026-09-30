from fastapi import APIRouter, Depends
from app.presentation.api.dependencias import requiere_administrador

from app.application.use_cases.campana.activar_campanas_programadas import ActivarCampanasProgramadas
from app.application.use_cases.campana.asignar_grupo_edad_a_campana import AsignarGrupoEdadACampana
from app.application.use_cases.campana.asignar_punto_a_campana import AsignarPuntoACampana
from app.application.use_cases.campana.crear_campana import CrearCampana
from app.application.use_cases.campana.eliminar_campana import EliminarCampana
from app.application.use_cases.campana.finalizar_campanas_vencidas import FinalizarCampanasVencidas
from app.application.use_cases.campana.listar_campanas import ListarCampanas
from app.application.use_cases.campana.listar_campanas_activas import ListarCampanasActivas
from app.application.use_cases.campana.obtener_campana import ObtenerCampana
from app.application.use_cases.campana.quitar_grupo_edad_de_campana import QuitarGrupoEdadDeCampana
from app.application.use_cases.campana.quitar_punto_de_campana import QuitarPuntoDeCampana
from app.domain.repositories.campana_repository import CampanaRepository
from app.domain.repositories.grupo_edad_repository import GrupoEdadRepository
from app.domain.repositories.punto_vacunacion_repository import PuntoVacunacionRepository
from app.domain.repositories.vacuna_repository import VacunaRepository
from app.presentation.api.dependencias import get_campana_repository, get_grupo_edad_repository, get_punto_vacunacion_repository, get_vacuna_repository, obtener_usuario_actual
from app.presentation.api.schemas.campana import AsignarGrupoEdadRequest, AsignarPuntoRequest, CampanaCreate, CampanaResponse


router = APIRouter(prefix="/campanas", tags=["Campañas"], dependencies=[Depends(obtener_usuario_actual)])


@router.post("/", response_model=CampanaResponse, status_code=201, dependencies=[Depends(requiere_administrador)])
def crear(
    datos: CampanaCreate,
    repo: CampanaRepository = Depends(get_campana_repository),
    grupo_edad_repo: GrupoEdadRepository = Depends(get_grupo_edad_repository),
    vacuna_repo: VacunaRepository = Depends(get_vacuna_repository),
):
    return CrearCampana(repo, grupo_edad_repo, vacuna_repo).ejecutar(**datos.model_dump())


@router.get("/", response_model=list[CampanaResponse])
def listar(repo: CampanaRepository = Depends(get_campana_repository)):
    return ListarCampanas(repo).ejecutar()


@router.get("/activas", response_model=list[CampanaResponse])
def listar_activas(repo: CampanaRepository = Depends(get_campana_repository)):
    return ListarCampanasActivas(repo).ejecutar()


@router.post("/activar-programadas", response_model=list[CampanaResponse], dependencies=[Depends(requiere_administrador)])
def activar_programadas(repo: CampanaRepository = Depends(get_campana_repository)):
    return ActivarCampanasProgramadas(repo).ejecutar()


@router.post("/finalizar-vencidas", response_model=list[CampanaResponse], dependencies=[Depends(requiere_administrador)])
def finalizar_vencidas(repo: CampanaRepository = Depends(get_campana_repository)):
    return FinalizarCampanasVencidas(repo).ejecutar()


@router.get("/{campana_id}", response_model=CampanaResponse)
def obtener(campana_id: int, repo: CampanaRepository = Depends(get_campana_repository)):
    return ObtenerCampana(repo).ejecutar(campana_id)


@router.post("/{campana_id}/asignar-punto", response_model=CampanaResponse, dependencies=[Depends(requiere_administrador)])
def asignar_punto(
    campana_id: int,
    datos: AsignarPuntoRequest,
    campana_repo: CampanaRepository = Depends(get_campana_repository),
    punto_repo: PuntoVacunacionRepository = Depends(get_punto_vacunacion_repository),
):
    return AsignarPuntoACampana(campana_repo, punto_repo).ejecutar(campana_id, datos.punto_id)


@router.delete("/{campana_id}/puntos/{punto_id}", response_model=CampanaResponse, dependencies=[Depends(requiere_administrador)])
def quitar_punto(
    campana_id: int,
    punto_id: int,
    campana_repo: CampanaRepository = Depends(get_campana_repository),
    punto_repo: PuntoVacunacionRepository = Depends(get_punto_vacunacion_repository),
):
    return QuitarPuntoDeCampana(campana_repo, punto_repo).ejecutar(campana_id, punto_id)


@router.post("/{campana_id}/asignar-grupo-edad", response_model=CampanaResponse, dependencies=[Depends(requiere_administrador)])
def asignar_grupo_edad(
    campana_id: int,
    datos: AsignarGrupoEdadRequest,
    campana_repo: CampanaRepository = Depends(get_campana_repository),
    grupo_repo: GrupoEdadRepository = Depends(get_grupo_edad_repository),
    vacuna_repo: VacunaRepository = Depends(get_vacuna_repository),
):
    return AsignarGrupoEdadACampana(campana_repo, grupo_repo, vacuna_repo).ejecutar(campana_id, datos.grupo_edad_id)


@router.delete("/{campana_id}/grupos-edad/{grupo_edad_id}", response_model=CampanaResponse, dependencies=[Depends(requiere_administrador)])
def quitar_grupo_edad(
    campana_id: int,
    grupo_edad_id: int,
    campana_repo: CampanaRepository = Depends(get_campana_repository),
):
    return QuitarGrupoEdadDeCampana(campana_repo).ejecutar(campana_id, grupo_edad_id)


@router.delete("/{campana_id}", status_code=204, dependencies=[Depends(requiere_administrador)])
def eliminar(campana_id: int, repo: CampanaRepository = Depends(get_campana_repository)):
    EliminarCampana(repo).ejecutar(campana_id)
