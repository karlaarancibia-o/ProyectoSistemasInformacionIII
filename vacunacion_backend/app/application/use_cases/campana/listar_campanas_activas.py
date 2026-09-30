from app.domain.entities.campana import Campana
from app.domain.repositories.campana_repository import CampanaRepository


class ListarCampanasActivas:
    """Evento 17: El administrador consulta las campañas activas."""

    def __init__(self, repo: CampanaRepository):
        self.repo = repo

    def ejecutar(self) -> list[Campana]:
        return self.repo.listar_activas()
