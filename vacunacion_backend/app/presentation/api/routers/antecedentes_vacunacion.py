from datetime import date

from fastapi import APIRouter, Depends
from app.presentation.api.dependencias import requiere_administrador, requiere_personal_salud

from app.application.use_cases.antecedente_vacunacion.eliminar_antecedente_vacunacion import EliminarAntecedenteVacunacion
from app.application.use_cases.antecedente_vacunacion.listar_antecedentes_vacunacion import ListarAntecedentesVacunacion
from app.application.use_cases.antecedente_vacunacion.obtener_antecedente_vacunacion import ObtenerAntecedenteVacunacion
from app.application.use_cases.antecedente_vacunacion.registrar_antecedente_vacunacion import RegistrarAntecedenteVacunacion
from app.domain.repositories.antecedente_vacunacion_repository import AntecedenteVacunacionRepository
from app.domain.repositories.paciente_repository import PacienteRepository
from app.presentation.api.dependencias import get_antecedente_vacunacion_repository, get_paciente_repository, obtener_usuario_actual
from pydantic import BaseModel, Field

from app.presentation.api.schemas.paciente import AntecedenteVacunacionResponse

class AntecedenteVacunacionRequest(BaseModel):
    paciente_id: int
    vacuna: str = Field(..., min_length=2, max_length=100)
    fecha_aplicacion: date
    numero_dosis: int = Field(..., gt=0)
    observaciones: str | None = None


router = APIRouter(prefix="/antecedentes-vacunacion", tags=["Antecedentes de Vacunación"], dependencies=[Depends(obtener_usuario_actual)])


@router.post("/", response_model=AntecedenteVacunacionResponse, status_code=201, dependencies=[Depends(requiere_personal_salud)])
def registrar(
    datos: AntecedenteVacunacionRequest,
    repo: AntecedenteVacunacionRepository = Depends(get_antecedente_vacunacion_repository),
    paciente_repo: PacienteRepository = Depends(get_paciente_repository),
):
    return RegistrarAntecedenteVacunacion(repo, paciente_repo).ejecutar(**datos.model_dump())


@router.get("/", response_model=list[AntecedenteVacunacionResponse], dependencies=[Depends(requiere_personal_salud)])
def listar(
    paciente_id: int | None = None,
    repo: AntecedenteVacunacionRepository = Depends(get_antecedente_vacunacion_repository),
):
    return ListarAntecedentesVacunacion(repo).ejecutar(paciente_id)


@router.get("/{antecedente_id}", response_model=AntecedenteVacunacionResponse, dependencies=[Depends(requiere_personal_salud)])
def obtener(antecedente_id: int, repo: AntecedenteVacunacionRepository = Depends(get_antecedente_vacunacion_repository)):
    return ObtenerAntecedenteVacunacion(repo).ejecutar(antecedente_id)


@router.delete("/{antecedente_id}", status_code=204, dependencies=[Depends(requiere_administrador)])
def eliminar(antecedente_id: int, repo: AntecedenteVacunacionRepository = Depends(get_antecedente_vacunacion_repository)):
    EliminarAntecedenteVacunacion(repo).ejecutar(antecedente_id)
