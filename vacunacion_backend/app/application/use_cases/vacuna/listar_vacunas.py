from app.domain.entities.vacuna import Vacuna
from app.domain.repositories.vacuna_repository import VacunaRepository


class ListarVacunas:
    def __init__(self, repo: VacunaRepository):
        self.repo = repo

    def ejecutar(self) -> list[Vacuna]:
        return self.repo.listar()
