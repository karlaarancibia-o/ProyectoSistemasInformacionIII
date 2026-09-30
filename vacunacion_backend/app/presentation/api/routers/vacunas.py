from fastapi import APIRouter, Depends
from app.presentation.api.dependencias import requiere_administrador

from app.application.use_cases.vacuna.actualizar_vacuna import ActualizarVacuna
from app.application.use_cases.vacuna.crear_vacuna import CrearVacuna
from app.application.use_cases.vacuna.eliminar_vacuna import EliminarVacuna
from app.application.use_cases.vacuna.listar_vacunas import ListarVacunas
from app.application.use_cases.vacuna.obtener_vacuna import ObtenerVacuna
from app.domain.repositories.grupo_edad_repository import GrupoEdadRepository
from app.domain.repositories.vacuna_repository import VacunaRepository
from app.presentation.api.dependencias import get_grupo_edad_repository, get_vacuna_repository, obtener_usuario_actual
from app.presentation.api.schemas.vacuna import VacunaCreate, VacunaResponse, VacunaUpdate

router = APIRouter(prefix="/vacunas", tags=["Vacunas"], dependencies=[Depends(obtener_usuario_actual)])


@router.post("/", response_model=VacunaResponse, status_code=201, dependencies=[Depends(requiere_administrador)])
def crear(datos: VacunaCreate, repo: VacunaRepository = Depends(get_vacuna_repository), grupo_edad_repo: GrupoEdadRepository = Depends(get_grupo_edad_repository)):
    return CrearVacuna(repo, grupo_edad_repo).ejecutar(**datos.model_dump())


@router.get("/", response_model=list[VacunaResponse])
def listar(repo: VacunaRepository = Depends(get_vacuna_repository)):
    return ListarVacunas(repo).ejecutar()


@router.get("/{vacuna_id}", response_model=VacunaResponse)
def obtener(vacuna_id: int, repo: VacunaRepository = Depends(get_vacuna_repository)):
    return ObtenerVacuna(repo).ejecutar(vacuna_id)


@router.put("/{vacuna_id}", response_model=VacunaResponse, dependencies=[Depends(requiere_administrador)])
def actualizar(vacuna_id: int, datos: VacunaUpdate, repo: VacunaRepository = Depends(get_vacuna_repository), grupo_edad_repo: GrupoEdadRepository = Depends(get_grupo_edad_repository)):
    return ActualizarVacuna(repo, grupo_edad_repo).ejecutar(vacuna_id, **datos.model_dump())


@router.delete("/{vacuna_id}", status_code=204, dependencies=[Depends(requiere_administrador)])
def eliminar(vacuna_id: int, repo: VacunaRepository = Depends(get_vacuna_repository)):
    EliminarVacuna(repo).ejecutar(vacuna_id)
