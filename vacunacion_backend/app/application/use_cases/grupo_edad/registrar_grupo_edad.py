from app.domain.entities.grupo_edad import GrupoEdad
from app.domain.exceptions import OperacionNoPermitidaError
from app.domain.repositories.grupo_edad_repository import GrupoEdadRepository


class RegistrarGrupoEdad:
    """Evento 2: El administrador registra los grupos de edad prioritarios.
    Los rangos de edad de los grupos no pueden superponerse, para que a cada
    persona le corresponda un único grupo."""

    def __init__(self, repo: GrupoEdadRepository):
        self.repo = repo

    def ejecutar(
        self,
        nombre: str,
        edad_min: int,
        edad_max: int,
        prioridad: int,
        descripcion: str | None = None,
    ) -> GrupoEdad:
        grupo = GrupoEdad(
            nombre=nombre,
            edad_min=edad_min,
            edad_max=edad_max,
            prioridad=prioridad,
            descripcion=descripcion,
        )
        for otro in self.repo.listar():
            if grupo.se_superpone_con(otro):
                raise OperacionNoPermitidaError(
                    f"El rango {edad_min}–{edad_max} se superpone con el grupo '{otro.nombre}' "
                    f"({otro.edad_min}–{otro.edad_max})"
                )
        return self.repo.crear(grupo)
