from app.application.use_cases.campana.obtener_campana import ObtenerCampana
from app.domain.repositories.campana_repository import CampanaRepository


class EliminarCampana:
    def __init__(self, repo: CampanaRepository):
        self.repo = repo

    def ejecutar(self, campana_id: int) -> None:
        ObtenerCampana(self.repo).ejecutar(campana_id)
        self.repo.eliminar(campana_id)
