from fastapi import APIRouter, Depends
from app.presentation.api.dependencias import requiere_administrador, requiere_personal_salud

from app.application.use_cases.antecedente_vacunacion.registrar_antecedente_vacunacion import RegistrarAntecedenteVacunacion
from app.application.use_cases.paciente.consultar_historial_paciente import ConsultarHistorialPaciente
from app.application.use_cases.paciente.eliminar_paciente import EliminarPaciente
from app.application.use_cases.paciente.listar_pacientes import ListarPacientes
from app.application.use_cases.paciente.obtener_paciente import ObtenerPaciente
from app.application.use_cases.paciente.registrar_paciente import RegistrarPaciente
from app.domain.repositories.antecedente_vacunacion_repository import AntecedenteVacunacionRepository
from app.domain.repositories.grupo_edad_repository import GrupoEdadRepository
from app.domain.repositories.paciente_repository import PacienteRepository
from app.domain.repositories.registro_vacunacion_repository import RegistroVacunacionRepository
from app.presentation.api.dependencias import get_antecedente_vacunacion_repository, get_grupo_edad_repository, get_paciente_repository, get_registro_vacunacion_repository, obtener_usuario_actual
from app.presentation.api.schemas.paciente import AntecedenteVacunacionCreate, AntecedenteVacunacionResponse, HistorialPacienteResponse, PacienteCreate, PacienteResponse

router = APIRouter(prefix="/pacientes", tags=["Pacientes"], dependencies=[Depends(obtener_usuario_actual)])


@router.post("/", response_model=PacienteResponse, status_code=201, dependencies=[Depends(requiere_personal_salud)])
def registrar(datos: PacienteCreate, repo: PacienteRepository = Depends(get_paciente_repository), grupo_edad_repo: GrupoEdadRepository = Depends(get_grupo_edad_repository)):
    return RegistrarPaciente(repo, grupo_edad_repo).ejecutar(**datos.model_dump())


@router.get("/", response_model=list[PacienteResponse], dependencies=[Depends(requiere_personal_salud)])
def listar(repo: PacienteRepository = Depends(get_paciente_repository)):
    return ListarPacientes(repo).ejecutar()


@router.get("/{paciente_id}", response_model=PacienteResponse, dependencies=[Depends(requiere_personal_salud)])
def obtener(paciente_id: int, repo: PacienteRepository = Depends(get_paciente_repository)):
    return ObtenerPaciente(repo).ejecutar(paciente_id)


@router.post("/{paciente_id}/antecedentes", response_model=AntecedenteVacunacionResponse, status_code=201, dependencies=[Depends(requiere_personal_salud)])
def registrar_antecedente(paciente_id: int, datos: AntecedenteVacunacionCreate, repo: AntecedenteVacunacionRepository = Depends(get_antecedente_vacunacion_repository), paciente_repo: PacienteRepository = Depends(get_paciente_repository)):
    return RegistrarAntecedenteVacunacion(repo, paciente_repo).ejecutar(paciente_id=paciente_id, **datos.model_dump())


@router.get("/{paciente_id}/historial", response_model=HistorialPacienteResponse, dependencies=[Depends(requiere_personal_salud)])
def consultar_historial(paciente_id: int, paciente_repo: PacienteRepository = Depends(get_paciente_repository), antecedente_repo: AntecedenteVacunacionRepository = Depends(get_antecedente_vacunacion_repository), registro_repo: RegistroVacunacionRepository = Depends(get_registro_vacunacion_repository)):
    return ConsultarHistorialPaciente(paciente_repo, antecedente_repo, registro_repo).ejecutar(paciente_id)


@router.delete("/{paciente_id}", status_code=204, dependencies=[Depends(requiere_administrador)])
def eliminar(paciente_id: int, repo: PacienteRepository = Depends(get_paciente_repository)):
    EliminarPaciente(repo).ejecutar(paciente_id)
