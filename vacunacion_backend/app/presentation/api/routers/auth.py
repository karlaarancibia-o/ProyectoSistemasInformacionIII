import os

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.application.interfaces.password_hasher import PasswordHasher
from app.application.interfaces.token_service import TokenService
from app.application.use_cases.auth.cambiar_estado_usuario import CambiarEstadoUsuario
from app.application.use_cases.auth.cambiar_rol_usuario import CambiarRolUsuario
from app.application.use_cases.auth.listar_usuarios import ListarUsuarios
from app.application.use_cases.auth.login_usuario import LoginUsuario
from app.application.use_cases.auth.registrar_usuario import RegistrarUsuario
from app.domain.entities.usuario import Usuario
from app.domain.repositories.usuario_repository import UsuarioRepository
from app.domain.roles import DESCRIPCION_ROLES
from app.presentation.api.dependencias import (
    get_password_hasher,
    get_token_service,
    get_usuario_repository,
    obtener_usuario_actual,
    obtener_usuario_opcional,
    requiere_administrador,
)
from app.presentation.api.schemas.usuario import (
    CambiarEstadoRequest,
    CambiarRolRequest,
    RolResponse,
    Token,
    UsuarioCreate,
    UsuarioResponse,
)

router = APIRouter(prefix="/auth", tags=["Autenticación"])


def _registro_publico_habilitado() -> bool:
    return os.getenv("REGISTRO_PUBLICO", "true").strip().lower() in ("1", "true", "si", "sí", "yes")


@router.post("/registro", response_model=UsuarioResponse, status_code=201)
def registrar(
    datos: UsuarioCreate,
    repo: UsuarioRepository = Depends(get_usuario_repository),
    hasher: PasswordHasher = Depends(get_password_hasher),
    solicitante: Usuario | None = Depends(obtener_usuario_opcional),
):
    """Sin token: crea una cuenta de personal de salud (si el registro público está
    habilitado). Con token de administrador: crea la cuenta con el rol indicado.
    Si el sistema no tiene administrador, la cuenta creada será administrador."""
    return RegistrarUsuario(repo, hasher, _registro_publico_habilitado()).ejecutar(
        datos.username, datos.password, datos.rol, solicitante
    )


@router.post("/login", response_model=Token)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    repo: UsuarioRepository = Depends(get_usuario_repository),
    hasher: PasswordHasher = Depends(get_password_hasher),
    tokens: TokenService = Depends(get_token_service),
):
    token = LoginUsuario(repo, hasher, tokens).ejecutar(form.username, form.password)
    return Token(access_token=token)


@router.get("/me", response_model=UsuarioResponse)
def usuario_actual(usuario=Depends(obtener_usuario_actual)):
    """Devuelve el usuario autenticado a partir del token JWT."""
    return usuario


@router.get("/roles", response_model=list[RolResponse])
def listar_roles():
    """Roles disponibles y qué puede hacer cada uno."""
    return [RolResponse(rol=r, descripcion=d) for r, d in DESCRIPCION_ROLES.items()]


@router.get("/usuarios", response_model=list[UsuarioResponse], dependencies=[Depends(requiere_administrador)])
def listar_usuarios(repo: UsuarioRepository = Depends(get_usuario_repository)):
    return ListarUsuarios(repo).ejecutar()


@router.patch("/usuarios/{usuario_id}/rol", response_model=UsuarioResponse, dependencies=[Depends(requiere_administrador)])
def cambiar_rol(usuario_id: int, datos: CambiarRolRequest, repo: UsuarioRepository = Depends(get_usuario_repository)):
    return CambiarRolUsuario(repo).ejecutar(usuario_id, datos.rol)


@router.patch("/usuarios/{usuario_id}/estado", response_model=UsuarioResponse)
def cambiar_estado(
    usuario_id: int,
    datos: CambiarEstadoRequest,
    repo: UsuarioRepository = Depends(get_usuario_repository),
    admin: Usuario = Depends(requiere_administrador),
):
    """Activa o desactiva una cuenta."""
    return CambiarEstadoUsuario(repo).ejecutar(usuario_id, datos.activo, admin)
