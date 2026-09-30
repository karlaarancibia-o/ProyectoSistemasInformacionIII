from fastapi import APIRouter, Depends
from app.presentation.api.dependencias import requiere_administrador

from app.application.use_cases.grupo_edad.actualizar_grupo_edad import ActualizarGrupoEdad
from app.application.use_cases.grupo_edad.editar_prioridad_grupo_edad import EditarPrioridadGrupoEdad
from app.application.use_cases.grupo_edad.eliminar_grupo_edad import EliminarGrupoEdad
from app.application.use_cases.grupo_edad.listar_grupos_edad import ListarGruposEdad
from app.application.use_cases.grupo_edad.obtener_grupo_edad import ObtenerGrupoEdad
from app.application.use_cases.grupo_edad.registrar_grupo_edad import RegistrarGrupoEdad
from app.domain.repositories.grupo_edad_repository import GrupoEdadRepository
from app.domain.repositories.paciente_repository import PacienteRepository
from app.presentation.api.dependencias import get_grupo_edad_repository, get_paciente_repository, obtener_usuario_actual
from app.presentation.api.schemas.grupo_edad import EditarPrioridadRequest, GrupoEdadCreate, GrupoEdadResponse, GrupoEdadUpdate

router = APIRouter(prefix="/grupos-edad", tags=["Grupos de Edad"], dependencies=[Depends(obtener_usuario_actual)])


@router.post("/", response_model=GrupoEdadResponse, status_code=201, dependencies=[Depends(requiere_administrador)])
def registrar(datos: GrupoEdadCreate, repo: GrupoEdadRepository = Depends(get_grupo_edad_repository)):
    return RegistrarGrupoEdad(repo).ejecutar(**datos.model_dump())


@router.get("/", response_model=list[GrupoEdadResponse])
def listar(repo: GrupoEdadRepository = Depends(get_grupo_edad_repository)):
    return ListarGruposEdad(repo).ejecutar()


@router.get("/{grupo_id}", response_model=GrupoEdadResponse)
def obtener(grupo_id: int, repo: GrupoEdadRepository = Depends(get_grupo_edad_repository)):
    return ObtenerGrupoEdad(repo).ejecutar(grupo_id)


@router.put("/{grupo_id}", response_model=GrupoEdadResponse, dependencies=[Depends(requiere_administrador)])
def actualizar(grupo_id: int, datos: GrupoEdadUpdate, repo: GrupoEdadRepository = Depends(get_grupo_edad_repository), paciente_repo: PacienteRepository = Depends(get_paciente_repository)):
    return ActualizarGrupoEdad(repo, paciente_repo).ejecutar(grupo_id, **datos.model_dump())


@router.patch("/{grupo_id}/prioridad", response_model=GrupoEdadResponse, dependencies=[Depends(requiere_administrador)])
def editar_prioridad(grupo_id: int, datos: EditarPrioridadRequest, repo: GrupoEdadRepository = Depends(get_grupo_edad_repository)):
    return EditarPrioridadGrupoEdad(repo).ejecutar(grupo_id, datos.nueva_prioridad)


@router.delete("/{grupo_id}", status_code=204, dependencies=[Depends(requiere_administrador)])
def eliminar(grupo_id: int, repo: GrupoEdadRepository = Depends(get_grupo_edad_repository)):
    EliminarGrupoEdad(repo).ejecutar(grupo_id)
