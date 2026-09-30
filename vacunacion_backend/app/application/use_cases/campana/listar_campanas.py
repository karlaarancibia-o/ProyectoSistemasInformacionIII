from app.domain.entities.campana import Campana
from app.domain.repositories.campana_repository import CampanaRepository


class ListarCampanas:
    def __init__(self, repo: CampanaRepository):
        self.repo = repo

    def ejecutar(self) -> list[Campana]:
        return self.repo.listar()
