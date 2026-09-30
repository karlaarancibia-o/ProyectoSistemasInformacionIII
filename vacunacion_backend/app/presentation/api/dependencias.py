"""Punto de ensamblaje: aquí (y solo aquí) se elige qué implementación
concreta de infrastructure recibe cada caso de uso de application.
"""
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.application.interfaces.password_hasher import PasswordHasher
from app.application.services.esquema_paciente import ServicioEsquemaPaciente
from app.application.interfaces.token_service import TokenService
from app.application.use_cases.auth.obtener_usuario_actual import ObtenerUsuarioActual
from app.domain.entities.usuario import Usuario
from app.domain.exceptions import NoAutenticadoError, PermisoDenegadoError
from app.domain.roles import LOGISTICA, PERSONAL_SALUD
from app.domain.repositories.antecedente_vacunacion_repository import (
    AntecedenteVacunacionRepository,
)
from app.domain.repositories.campana_repository import CampanaRepository
from app.domain.repositories.grupo_edad_repository import GrupoEdadRepository
from app.domain.repositories.horario_atencion_repository import (
    HorarioAtencionRepository,
)
from app.domain.repositories.lote_dosis_repository import LoteDosisRepository
from app.domain.repositories.esquema_vacunacion_repository import EsquemaVacunacionRepository
from app.domain.repositories.movimiento_stock_repository import MovimientoStockRepository
from app.domain.repositories.vacuna_repository import VacunaRepository
from app.domain.repositories.paciente_repository import PacienteRepository
from app.domain.repositories.punto_vacunacion_repository import (
    PuntoVacunacionRepository,
)
from app.domain.repositories.registro_temperatura_repository import (
    RegistroTemperaturaRepository,
)
from app.domain.repositories.registro_vacunacion_repository import (
    RegistroVacunacionRepository,
)
from app.domain.repositories.usuario_repository import UsuarioRepository
from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.sqlalchemy_antecedente_vacunacion_repository import (
    SqlAlchemyAntecedenteVacunacionRepository,
)
from app.infrastructure.repositories.sqlalchemy_campana_repository import (
    SqlAlchemyCampanaRepository,
)
from app.infrastructure.repositories.sqlalchemy_grupo_edad_repository import (
    SqlAlchemyGrupoEdadRepository,
)
from app.infrastructure.repositories.sqlalchemy_horario_atencion_repository import (
    SqlAlchemyHorarioAtencionRepository,
)
from app.infrastructure.repositories.sqlalchemy_esquema_vacunacion_repository import (
    SqlAlchemyEsquemaVacunacionRepository,
)
from app.infrastructure.repositories.sqlalchemy_movimiento_stock_repository import (
    SqlAlchemyMovimientoStockRepository,
)
from app.infrastructure.repositories.sqlalchemy_vacuna_repository import (
    SqlAlchemyVacunaRepository,
)
from app.infrastructure.repositories.sqlalchemy_lote_dosis_repository import (
    SqlAlchemyLoteDosisRepository,
)
from app.infrastructure.repositories.sqlalchemy_paciente_repository import (
    SqlAlchemyPacienteRepository,
)
from app.infrastructure.repositories.sqlalchemy_punto_vacunacion_repository import (
    SqlAlchemyPuntoVacunacionRepository,
)
from app.infrastructure.repositories.sqlalchemy_registro_temperatura_repository import (
    SqlAlchemyRegistroTemperaturaRepository,
)
from app.infrastructure.repositories.sqlalchemy_registro_vacunacion_repository import (
    SqlAlchemyRegistroVacunacionRepository,
)
from app.infrastructure.repositories.sqlalchemy_usuario_repository import (
    SqlAlchemyUsuarioRepository,
)
from app.infrastructure.security.password_hasher import BcryptPasswordHasher
from app.infrastructure.security.token_service import JwtTokenService
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
oauth2_scheme_opcional = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)


# ---- repositorios (devuelven la INTERFAZ del dominio) ----
def get_usuario_repository(db: Session = Depends(get_db)) -> UsuarioRepository:
    return SqlAlchemyUsuarioRepository(db)


def get_campana_repository(db: Session = Depends(get_db)) -> CampanaRepository:
    return SqlAlchemyCampanaRepository(db)


def get_grupo_edad_repository(db: Session = Depends(get_db)) -> GrupoEdadRepository:
    return SqlAlchemyGrupoEdadRepository(db)


def get_punto_vacunacion_repository(
    db: Session = Depends(get_db),
) -> PuntoVacunacionRepository:
    return SqlAlchemyPuntoVacunacionRepository(db)


def get_horario_atencion_repository(
    db: Session = Depends(get_db),
) -> HorarioAtencionRepository:
    return SqlAlchemyHorarioAtencionRepository(db)


def get_paciente_repository(db: Session = Depends(get_db)) -> PacienteRepository:
    return SqlAlchemyPacienteRepository(db)


def get_antecedente_vacunacion_repository(
    db: Session = Depends(get_db),
) -> AntecedenteVacunacionRepository:
    return SqlAlchemyAntecedenteVacunacionRepository(db)


def get_lote_dosis_repository(db: Session = Depends(get_db)) -> LoteDosisRepository:
    return SqlAlchemyLoteDosisRepository(db)


def get_esquema_vacunacion_repository(
    db: Session = Depends(get_db),
) -> EsquemaVacunacionRepository:
    return SqlAlchemyEsquemaVacunacionRepository(db)


def get_vacuna_repository(db: Session = Depends(get_db)) -> VacunaRepository:
    return SqlAlchemyVacunaRepository(db)


def get_movimiento_stock_repository(
    db: Session = Depends(get_db),
) -> MovimientoStockRepository:
    return SqlAlchemyMovimientoStockRepository(db)


def get_registro_temperatura_repository(
    db: Session = Depends(get_db),
) -> RegistroTemperaturaRepository:
    return SqlAlchemyRegistroTemperaturaRepository(db)


def get_registro_vacunacion_repository(
    db: Session = Depends(get_db),
) -> RegistroVacunacionRepository:
    return SqlAlchemyRegistroVacunacionRepository(db)



# ---- servicios de aplicación ----
def get_servicio_esquema_paciente(
    registro_repo: RegistroVacunacionRepository = Depends(get_registro_vacunacion_repository),
    antecedente_repo: AntecedenteVacunacionRepository = Depends(get_antecedente_vacunacion_repository),
    esquema_repo: EsquemaVacunacionRepository = Depends(get_esquema_vacunacion_repository),
    grupo_repo: GrupoEdadRepository = Depends(get_grupo_edad_repository),
    vacuna_repo: VacunaRepository = Depends(get_vacuna_repository),
) -> ServicioEsquemaPaciente:
    return ServicioEsquemaPaciente(
        registro_repo, antecedente_repo, esquema_repo, grupo_repo, vacuna_repo
    )


# ---- seguridad ----
def get_password_hasher() -> PasswordHasher:
    return BcryptPasswordHasher()


def get_token_service() -> TokenService:
    return JwtTokenService()


# ---- usuario autenticado ----
def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    repo: UsuarioRepository = Depends(get_usuario_repository),
    tokens: TokenService = Depends(get_token_service),
) -> Usuario:
    return ObtenerUsuarioActual(repo, tokens).ejecutar(token)


def obtener_usuario_opcional(
    token: str | None = Depends(oauth2_scheme_opcional),
    repo: UsuarioRepository = Depends(get_usuario_repository),
    tokens: TokenService = Depends(get_token_service),
) -> Usuario | None:
    """Usuario autenticado si envía un token válido; None si no (registro público)."""
    if not token:
        return None
    try:
        return ObtenerUsuarioActual(repo, tokens).ejecutar(token)
    except NoAutenticadoError:
        return None


def requerir_roles(*roles_permitidos: str):
    """Exige que el usuario tenga alguno de los roles indicados.
    El administrador siempre tiene acceso."""

    def verificar(usuario: Usuario = Depends(obtener_usuario_actual)) -> Usuario:
        if not usuario.puede(*roles_permitidos):
            raise PermisoDenegadoError(
                "Su rol no tiene permisos para esta acción"
            )
        return usuario

    return verificar


# Dependencias listas para usar en los endpoints (el administrador entra en todas)
requiere_administrador = requerir_roles()
requiere_personal_salud = requerir_roles(PERSONAL_SALUD)
requiere_logistica = requerir_roles(LOGISTICA)
