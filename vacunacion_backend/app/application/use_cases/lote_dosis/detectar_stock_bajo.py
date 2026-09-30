from app.domain.entities.lote_dosis import LoteDosis
from app.domain.repositories.lote_dosis_repository import LoteDosisRepository


class DetectarStockBajo:
    """Evento 23: El stock desciende al umbral mínimo definido."""

    def __init__(self, repo: LoteDosisRepository):
        self.repo = repo

    def ejecutar(self) -> list[LoteDosis]:
        return self.repo.listar_con_stock_bajo()
