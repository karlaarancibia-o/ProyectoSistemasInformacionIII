from app.application.use_cases.vacuna.obtener_vacuna import ObtenerVacuna
from app.domain.repositories.vacuna_repository import VacunaRepository


class EliminarVacuna:
    def __init__(self, repo: VacunaRepository):
        self.repo = repo

    def ejecutar(self, vacuna_id: int) -> None:
        # si no existe, ObtenerVacuna lanza NoEncontradoError
        ObtenerVacuna(self.repo).ejecutar(vacuna_id)
        self.repo.eliminar(vacuna_id)
