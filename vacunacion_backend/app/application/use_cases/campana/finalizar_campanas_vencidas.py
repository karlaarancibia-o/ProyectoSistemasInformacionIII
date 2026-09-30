from datetime import date

from app.domain.entities.campana import Campana
from app.domain.repositories.campana_repository import CampanaRepository


class FinalizarCampanasVencidas:
    """Evento 13 (temporal): Se alcanza la fecha de finalización de una
    campaña."""

    def __init__(self, repo: CampanaRepository):
        self.repo = repo

    def ejecutar(self) -> list[Campana]:
        hoy = date.today()
        campanas = self.repo.listar_activas_hasta(hoy)
        finalizadas = []
        for campana in campanas:
            campana.finalizar(hoy)
            finalizadas.append(self.repo.actualizar(campana))
        return finalizadas
