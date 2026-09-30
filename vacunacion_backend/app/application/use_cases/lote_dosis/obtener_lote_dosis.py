from app.domain.entities.lote_dosis import LoteDosis
from app.domain.exceptions import NoEncontradoError
from app.domain.repositories.lote_dosis_repository import LoteDosisRepository


class ObtenerLoteDosis:
    def __init__(self, repo: LoteDosisRepository):
        self.repo = repo

    def ejecutar(self, lote_id: int) -> LoteDosis:
        lote = self.repo.obtener_por_id(lote_id)
        if not lote:
            raise NoEncontradoError("Lote de dosis no encontrado")
        return lote
