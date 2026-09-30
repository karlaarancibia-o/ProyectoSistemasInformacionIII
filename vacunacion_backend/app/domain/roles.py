"""Roles del sistema.

- administrador: acceso total (incluye todo lo de los otros dos roles).
- personal_salud: pacientes, antecedentes, registro de dosis aplicadas y
  consulta de historial / dosis y refuerzos pendientes.
- logistica: stock de dosis (entradas, salidas, lotes), movimientos de
  stock y cadena de frío (temperaturas).
"""

from app.domain.exceptions import DatosInvalidosError

ADMINISTRADOR = "administrador"
PERSONAL_SALUD = "personal_salud"
LOGISTICA = "logistica"

ROLES_VALIDOS = (ADMINISTRADOR, PERSONAL_SALUD, LOGISTICA)

DESCRIPCION_ROLES = {
    ADMINISTRADOR: "Acceso total: catálogo, campañas, usuarios, reportes y todas las funciones de los demás roles",
    PERSONAL_SALUD: "Registra pacientes, antecedentes y dosis aplicadas; consulta historial y pendientes",
    LOGISTICA: "Gestiona stock de dosis, movimientos de stock y cadena de frío",
}

# valores que existían antes de definir los roles
_ALIAS_LEGADOS = {"operador": PERSONAL_SALUD, "admin": ADMINISTRADOR}


def normalizar_rol(rol: str | None) -> str:
    """Convierte un rol (posiblemente legado) a uno válido.
    Un valor desconocido se trata como el rol de menor alcance."""
    if rol is None:
        return PERSONAL_SALUD
    rol = rol.strip().lower()
    if rol in ROLES_VALIDOS:
        return rol
    return _ALIAS_LEGADOS.get(rol, PERSONAL_SALUD)


def validar_rol(rol: str | None) -> str:
    """Igual que normalizar_rol pero rechaza valores que no existen."""
    if rol is None:
        return PERSONAL_SALUD
    limpio = rol.strip().lower()
    if limpio in ROLES_VALIDOS or limpio in _ALIAS_LEGADOS:
        return normalizar_rol(limpio)
    raise DatosInvalidosError(
        f"Rol inválido. Roles disponibles: {', '.join(ROLES_VALIDOS)}"
    )
