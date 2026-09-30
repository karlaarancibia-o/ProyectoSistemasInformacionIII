from datetime import date

from app.domain.entities.campana import Campana
from app.domain.repositories.campana_repository import CampanaRepository


class ActivarCampanasProgramadas:
    """Evento 12 (temporal): Se alcanza la fecha de inicio de una campaña.

    Pensado para ser disparado por un scheduler (cron/job periódico) que
    revisa qué campañas planificadas ya deben activarse.
    """

    def __init__(self, repo: CampanaRepository):
        self.repo = repo

    def ejecutar(self) -> list[Campana]:
        hoy = date.today()
        campanas = self.repo.listar_planificadas_desde(hoy)
        activadas = []
        for campana in campanas:
            campana.activar(hoy)
            activadas.append(self.repo.actualizar(campana))
        return activadas
