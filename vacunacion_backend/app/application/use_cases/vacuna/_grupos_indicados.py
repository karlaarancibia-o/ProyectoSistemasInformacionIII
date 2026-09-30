from app.domain.exceptions import DatosInvalidosError, NoEncontradoError
from app.domain.repositories.grupo_edad_repository import GrupoEdadRepository


def validar_grupos_indicados(grupo_edad_repo: GrupoEdadRepository, grupo_edad_ids: list[int]) -> list[int]:
    """Toda vacuna se indica para al menos un grupo de edad YA CREADO
    (no se escriben edades a mano). Devuelve los ids sin repetir."""
    ids = list(dict.fromkeys(grupo_edad_ids or []))
    if not ids:
        raise DatosInvalidosError("Seleccione al menos un grupo de edad para la vacuna")
    for grupo_id in ids:
        if not grupo_edad_repo.obtener_por_id(grupo_id):
            raise NoEncontradoError(f"Grupo de edad {grupo_id} no encontrado")
    return ids
