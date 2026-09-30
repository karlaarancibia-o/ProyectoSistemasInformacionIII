from datetime import date

from app.domain.entities.lote_dosis import LoteDosis
from app.domain.repositories.lote_dosis_repository import LoteDosisRepository


class DetectarLotesVencidos:
    """Evento 16 (temporal): Se alcanza la fecha de vencimiento de un lote
    de vacunas."""

    def __init__(self, repo: LoteDosisRepository):
        self.repo = repo

    def ejecutar(self) -> list[LoteDosis]:
        return self.repo.listar_vencidos(date.today())
