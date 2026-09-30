from fastapi import APIRouter, Depends
from app.presentation.api.dependencias import requiere_administrador, requiere_logistica

from app.application.use_cases.horario_atencion.actualizar_horario_atencion import ActualizarHorarioAtencion
from app.application.use_cases.horario_atencion.definir_horario_atencion import DefinirHorarioAtencion
from app.application.use_cases.horario_atencion.eliminar_horario_atencion import EliminarHorarioAtencion
from app.application.use_cases.horario_atencion.listar_horarios_atencion import ListarHorariosAtencion
from app.application.use_cases.horario_atencion.obtener_horario_atencion import ObtenerHorarioAtencion
from app.application.use_cases.punto_vacunacion.actualizar_punto_vacunacion import ActualizarPuntoVacunacion
from app.application.use_cases.punto_vacunacion.crear_punto_vacunacion import CrearPuntoVacunacion
from app.application.use_cases.punto_vacunacion.detectar_puntos_sin_stock import DetectarPuntosSinStock
from app.application.use_cases.punto_vacunacion.eliminar_punto_vacunacion import EliminarPuntoVacunacion
from app.application.use_cases.punto_vacunacion.listar_puntos_vacunacion import ListarPuntosVacunacion
from app.application.use_cases.punto_vacunacion.obtener_punto_vacunacion import ObtenerPuntoVacunacion
from app.application.use_cases.punto_vacunacion.obtener_puntos_pendientes_registro_temperatura import ObtenerPuntosPendientesRegistroTemperatura
from app.domain.repositories.horario_atencion_repository import HorarioAtencionRepository
from app.domain.repositories.punto_vacunacion_repository import PuntoVacunacionRepository
from app.domain.repositories.lote_dosis_repository import LoteDosisRepository
from app.domain.repositories.registro_temperatura_repository import RegistroTemperaturaRepository
from app.presentation.api.dependencias import get_horario_atencion_repository, get_lote_dosis_repository, get_punto_vacunacion_repository, get_registro_temperatura_repository, obtener_usuario_actual
from app.presentation.api.schemas.horario_atencion import HorarioAtencionCreate, HorarioAtencionResponse
from app.presentation.api.schemas.punto_vacunacion import PuntoVacunacionCreate, PuntoVacunacionResponse, PuntoVacunacionUpdate

router = APIRouter(prefix="/puntos-vacunacion", tags=["Puntos de Vacunación"], dependencies=[Depends(obtener_usuario_actual)])


@router.post("/", response_model=PuntoVacunacionResponse, status_code=201, dependencies=[Depends(requiere_administrador)])
def crear(datos: PuntoVacunacionCreate, repo: PuntoVacunacionRepository = Depends(get_punto_vacunacion_repository)):
    return CrearPuntoVacunacion(repo).ejecutar(**datos.model_dump())


@router.get("/", response_model=list[PuntoVacunacionResponse])
def listar(repo: PuntoVacunacionRepository = Depends(get_punto_vacunacion_repository)):
    return ListarPuntosVacunacion(repo).ejecutar()


@router.get("/sin-stock", response_model=list[PuntoVacunacionResponse], dependencies=[Depends(requiere_logistica)])
def sin_stock(punto_repo: PuntoVacunacionRepository = Depends(get_punto_vacunacion_repository), lote_repo: LoteDosisRepository = Depends(get_lote_dosis_repository)):
    return DetectarPuntosSinStock(punto_repo, lote_repo).ejecutar()


@router.get("/temperaturas-pendientes", response_model=list[PuntoVacunacionResponse], dependencies=[Depends(requiere_logistica)])
def temperaturas_pendientes(punto_repo: PuntoVacunacionRepository = Depends(get_punto_vacunacion_repository), temperatura_repo: RegistroTemperaturaRepository = Depends(get_registro_temperatura_repository)):
    return ObtenerPuntosPendientesRegistroTemperatura(punto_repo, temperatura_repo).ejecutar()


@router.get("/{punto_id}", response_model=PuntoVacunacionResponse)
def obtener(punto_id: int, repo: PuntoVacunacionRepository = Depends(get_punto_vacunacion_repository)):
    return ObtenerPuntoVacunacion(repo).ejecutar(punto_id)


@router.patch("/{punto_id}", response_model=PuntoVacunacionResponse, dependencies=[Depends(requiere_administrador)])
def actualizar(punto_id: int, datos: PuntoVacunacionUpdate, repo: PuntoVacunacionRepository = Depends(get_punto_vacunacion_repository)):
    return ActualizarPuntoVacunacion(repo).ejecutar(punto_id, **datos.model_dump())


@router.delete("/{punto_id}", status_code=204, dependencies=[Depends(requiere_administrador)])
def eliminar(punto_id: int, repo: PuntoVacunacionRepository = Depends(get_punto_vacunacion_repository)):
    EliminarPuntoVacunacion(repo).ejecutar(punto_id)


@router.post("/{punto_id}/horarios", response_model=HorarioAtencionResponse, status_code=201, dependencies=[Depends(requiere_administrador)])
def definir_horario(punto_id: int, datos: HorarioAtencionCreate, repo: HorarioAtencionRepository = Depends(get_horario_atencion_repository), punto_repo: PuntoVacunacionRepository = Depends(get_punto_vacunacion_repository)):
    return DefinirHorarioAtencion(repo, punto_repo).ejecutar(punto_id, **datos.model_dump())


@router.get("/{punto_id}/horarios", response_model=list[HorarioAtencionResponse])
def listar_horarios(punto_id: int, repo: HorarioAtencionRepository = Depends(get_horario_atencion_repository)):
    return ListarHorariosAtencion(repo).ejecutar(punto_id)


@router.get("/{punto_id}/horarios/{horario_id}", response_model=HorarioAtencionResponse)
def obtener_horario(horario_id: int, repo: HorarioAtencionRepository = Depends(get_horario_atencion_repository)):
    return ObtenerHorarioAtencion(repo).ejecutar(horario_id)


@router.patch("/{punto_id}/horarios/{horario_id}", response_model=HorarioAtencionResponse, dependencies=[Depends(requiere_administrador)])
def actualizar_horario(horario_id: int, datos: HorarioAtencionCreate, repo: HorarioAtencionRepository = Depends(get_horario_atencion_repository)):
    return ActualizarHorarioAtencion(repo).ejecutar(horario_id, **datos.model_dump())


@router.delete("/{punto_id}/horarios/{horario_id}", status_code=204, dependencies=[Depends(requiere_administrador)])
def eliminar_horario(horario_id: int, repo: HorarioAtencionRepository = Depends(get_horario_atencion_repository)):
    EliminarHorarioAtencion(repo).ejecutar(horario_id)
