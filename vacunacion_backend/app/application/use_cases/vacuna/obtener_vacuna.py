from app.domain.entities.vacuna import Vacuna
from app.domain.exceptions import NoEncontradoError
from app.domain.repositories.vacuna_repository import VacunaRepository


class ObtenerVacuna:
    def __init__(self, repo: VacunaRepository):
        self.repo = repo

    def ejecutar(self, vacuna_id: int) -> Vacuna:
        vacuna = self.repo.obtener_por_id(vacuna_id)
        if not vacuna:
            raise NoEncontradoError("Vacuna no encontrada")
        return vacuna
