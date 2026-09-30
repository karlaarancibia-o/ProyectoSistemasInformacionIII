from app.application.use_cases.lote_dosis.obtener_lote_dosis import ObtenerLoteDosis
from app.domain.repositories.lote_dosis_repository import LoteDosisRepository


class EliminarLoteDosis:
    def __init__(self, repo: LoteDosisRepository):
        self.repo = repo

    def ejecutar(self, lote_id: int) -> None:
        ObtenerLoteDosis(self.repo).ejecutar(lote_id)
        self.repo.eliminar(lote_id)
