from dataclasses import dataclass

from app.domain.exceptions import DatosInvalidosError
from app.domain.roles import ADMINISTRADOR, PERSONAL_SALUD, ROLES_VALIDOS


@dataclass
class Usuario:
    username: str
    password_hash: str
    rol: str = PERSONAL_SALUD
    activo: bool = True
    id: int | None = None

    def __post_init__(self):
        if not self.username.strip():
            raise DatosInvalidosError("El nombre de usuario es obligatorio")
        if self.rol not in ROLES_VALIDOS:
            raise DatosInvalidosError(
                f"Rol inválido. Roles disponibles: {', '.join(ROLES_VALIDOS)}"
            )

    @property
    def es_administrador(self) -> bool:
        return self.rol == ADMINISTRADOR

    def puede(self, *roles_permitidos: str) -> bool:
        """El administrador puede todo; los demás solo si su rol está en la lista."""
        return self.es_administrador or self.rol in roles_permitidos
