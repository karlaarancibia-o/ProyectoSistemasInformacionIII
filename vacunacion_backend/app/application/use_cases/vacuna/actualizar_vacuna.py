from app.application.use_cases.vacuna._grupos_indicados import validar_grupos_indicados
from app.domain.entities.vacuna import Vacuna
from app.domain.exceptions import NoEncontradoError
from app.domain.repositories.grupo_edad_repository import GrupoEdadRepository
from app.domain.repositories.vacuna_repository import VacunaRepository


class ActualizarVacuna:
    """El administrador edita los datos de una vacuna del catálogo
    (incluido su estado activa/inactiva)."""

    def __init__(self, repo: VacunaRepository, grupo_edad_repo: GrupoEdadRepository):
        self.repo = repo
        self.grupo_edad_repo = grupo_edad_repo

    def ejecutar(
        self,
        vacuna_id: int,
        nombre: str,
        fabricante: str,
        tipo: str,
        temperatura_minima: float,
        temperatura_maxima: float,
        grupo_edad_ids: list[int],
        descripcion: str | None = None,
        estado: str = "activa",
    ) -> Vacuna:
        if not self.repo.obtener_por_id(vacuna_id):
            raise NoEncontradoError("Vacuna no encontrada")

        grupo_edad_ids = validar_grupos_indicados(self.grupo_edad_repo, grupo_edad_ids)

        vacuna = Vacuna(  # revalida todas las invariantes
            id=vacuna_id,
            nombre=nombre,
            fabricante=fabricante,
            tipo=tipo,
            temperatura_minima=temperatura_minima,
            temperatura_maxima=temperatura_maxima,
            descripcion=descripcion,
            estado=estado,
            grupo_edad_ids=grupo_edad_ids,
        )
        return self.repo.actualizar(vacuna)
