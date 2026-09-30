from app.domain.entities.campana import Campana
from app.domain.exceptions import NoEncontradoError
from app.domain.repositories.campana_repository import CampanaRepository


class ObtenerCampana:
    def __init__(self, repo: CampanaRepository):
        self.repo = repo

    def ejecutar(self, campana_id: int) -> Campana:
        campana = self.repo.obtener_por_id(campana_id)
        if not campana:
            raise NoEncontradoError("Campaña no encontrada")
        return campana
