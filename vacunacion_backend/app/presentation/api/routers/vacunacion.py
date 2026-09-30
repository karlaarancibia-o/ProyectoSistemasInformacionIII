from fastapi import APIRouter, Depends
from app.presentation.api.dependencias import requiere_administrador, requiere_personal_salud

from app.application.use_cases.registro_vacunacion.consultar_dosis_pendientes import ConsultarDosisPendientes
from app.application.use_cases.registro_vacunacion.consultar_refuerzos_pendientes import ConsultarRefuerzosPendientes
from app.application.use_cases.registro_vacunacion.detectar_pacientes_con_dosis_pendiente import DetectarPacientesConDosisPendiente
from app.application.use_cases.registro_vacunacion.detectar_pacientes_con_refuerzo_pendiente import DetectarPacientesConRefuerzoPendiente
from app.application.use_cases.registro_vacunacion.eliminar_registro_vacunacion import EliminarRegistroVacunacion
from app.application.use_cases.registro_vacunacion.listar_registros_vacunacion import ListarRegistrosVacunacion
from app.application.use_cases.registro_vacunacion.obtener_registro_vacunacion import ObtenerRegistroVacunacion
from app.application.use_cases.registro_vacunacion.registrar_dosis_aplicada import RegistrarDosisAplicada
from app.application.services.esquema_paciente import ServicioEsquemaPaciente
from app.domain.entities.usuario import Usuario
from app.domain.repositories.campana_repository import CampanaRepository
from app.domain.repositories.movimiento_stock_repository import MovimientoStockRepository
from app.domain.repositories.punto_vacunacion_repository import PuntoVacunacionRepository
from app.domain.repositories.lote_dosis_repository import LoteDosisRepository
from app.domain.repositories.paciente_repository import PacienteRepository
from app.domain.repositories.registro_vacunacion_repository import RegistroVacunacionRepository
from app.presentation.api.dependencias import get_campana_repository, get_lote_dosis_repository, get_movimiento_stock_repository, get_paciente_repository, get_punto_vacunacion_repository, get_registro_vacunacion_repository, get_servicio_esquema_paciente, obtener_usuario_actual
from app.presentation.api.schemas.registro_vacunacion import EsquemaVacunacionResponse, PacienteConEsquemaResponse, RegistrarDosisAplicadaRequest, RegistroVacunacionResponse

router = APIRouter(prefix="/vacunacion", tags=["Registro de Vacunación"], dependencies=[Depends(obtener_usuario_actual)])


@router.post("/dosis-aplicadas", response_model=RegistroVacunacionResponse, status_code=201, dependencies=[Depends(requiere_personal_salud)])
def registrar_dosis_aplicada(datos: RegistrarDosisAplicadaRequest, registro_repo: RegistroVacunacionRepository = Depends(get_registro_vacunacion_repository), paciente_repo: PacienteRepository = Depends(get_paciente_repository), campana_repo: CampanaRepository = Depends(get_campana_repository), lote_repo: LoteDosisRepository = Depends(get_lote_dosis_repository), punto_repo: PuntoVacunacionRepository = Depends(get_punto_vacunacion_repository), movimiento_repo: MovimientoStockRepository = Depends(get_movimiento_stock_repository), servicio: ServicioEsquemaPaciente = Depends(get_servicio_esquema_paciente), usuario: Usuario = Depends(obtener_usuario_actual)):
    """Registra una dosis aplicada. El número de dosis y si es refuerzo los determina el esquema."""
    return RegistrarDosisAplicada(registro_repo, paciente_repo, campana_repo, lote_repo, punto_repo, movimiento_repo, servicio).ejecutar(**datos.model_dump(), usuario_id=usuario.id)


@router.get("/registros", response_model=list[RegistroVacunacionResponse], dependencies=[Depends(requiere_personal_salud)])
def listar_registros(repo: RegistroVacunacionRepository = Depends(get_registro_vacunacion_repository)):
    return ListarRegistrosVacunacion(repo).ejecutar()


@router.get("/registros/{registro_id}", response_model=RegistroVacunacionResponse, dependencies=[Depends(requiere_personal_salud)])
def obtener_registro(registro_id: int, repo: RegistroVacunacionRepository = Depends(get_registro_vacunacion_repository)):
    return ObtenerRegistroVacunacion(repo).ejecutar(registro_id)


@router.delete("/registros/{registro_id}", status_code=204, dependencies=[Depends(requiere_administrador)])
def eliminar_registro(registro_id: int, repo: RegistroVacunacionRepository = Depends(get_registro_vacunacion_repository), lote_repo: LoteDosisRepository = Depends(get_lote_dosis_repository), movimiento_repo: MovimientoStockRepository = Depends(get_movimiento_stock_repository), usuario: Usuario = Depends(obtener_usuario_actual)):
    EliminarRegistroVacunacion(repo, lote_repo, movimiento_repo).ejecutar(registro_id, usuario_id=usuario.id)


@router.get("/pacientes/{paciente_id}/dosis-pendientes", response_model=EsquemaVacunacionResponse, dependencies=[Depends(requiere_personal_salud)])
def consultar_dosis_pendientes(paciente_id: int, vacuna_id: int, paciente_repo: PacienteRepository = Depends(get_paciente_repository), servicio: ServicioEsquemaPaciente = Depends(get_servicio_esquema_paciente)):
    return ConsultarDosisPendientes(paciente_repo, servicio).ejecutar(paciente_id, vacuna_id)


@router.get("/pacientes/{paciente_id}/refuerzo-pendiente", response_model=bool, dependencies=[Depends(requiere_personal_salud)])
def consultar_refuerzo_pendiente(paciente_id: int, vacuna_id: int, paciente_repo: PacienteRepository = Depends(get_paciente_repository), servicio: ServicioEsquemaPaciente = Depends(get_servicio_esquema_paciente)):
    return ConsultarRefuerzosPendientes(paciente_repo, servicio).ejecutar(paciente_id, vacuna_id)


@router.get("/dosis-pendientes/pacientes", response_model=list[PacienteConEsquemaResponse], dependencies=[Depends(requiere_personal_salud)])
def detectar_pacientes_con_dosis_pendiente(vacuna_id: int, paciente_repo: PacienteRepository = Depends(get_paciente_repository), servicio: ServicioEsquemaPaciente = Depends(get_servicio_esquema_paciente)):
    return DetectarPacientesConDosisPendiente(paciente_repo, servicio).ejecutar(vacuna_id)


@router.get("/refuerzos-pendientes/pacientes", response_model=list[PacienteConEsquemaResponse], dependencies=[Depends(requiere_personal_salud)])
def detectar_pacientes_con_refuerzo_pendiente(vacuna_id: int, paciente_repo: PacienteRepository = Depends(get_paciente_repository), servicio: ServicioEsquemaPaciente = Depends(get_servicio_esquema_paciente)):
    return DetectarPacientesConRefuerzoPendiente(paciente_repo, servicio).ejecutar(vacuna_id)
