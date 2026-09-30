from app.application.use_cases.vacuna._grupos_indicados import validar_grupos_indicados
from app.domain.entities.vacuna import Vacuna
from app.domain.repositories.grupo_edad_repository import GrupoEdadRepository
from app.domain.repositories.vacuna_repository import VacunaRepository


class CrearVacuna:
    """El administrador registra una vacuna en el catálogo del sistema, indicando
    a qué grupos de edad (ya creados) está dirigida."""

    def __init__(self, repo: VacunaRepository, grupo_edad_repo: GrupoEdadRepository):
        self.repo = repo
        self.grupo_edad_repo = grupo_edad_repo

    def ejecutar(
        self,
        nombre: str,
        fabricante: str,
        tipo: str,
        temperatura_minima: float,
        temperatura_maxima: float,
        grupo_edad_ids: list[int],
        descripcion: str | None = None,
    ) -> Vacuna:
        grupo_edad_ids = validar_grupos_indicados(self.grupo_edad_repo, grupo_edad_ids)
        vacuna = Vacuna(
            nombre=nombre,
            fabricante=fabricante,
            tipo=tipo,
            temperatura_minima=temperatura_minima,
            temperatura_maxima=temperatura_maxima,
            descripcion=descripcion,
            grupo_edad_ids=grupo_edad_ids,
        )
        return self.repo.crear(vacuna)
