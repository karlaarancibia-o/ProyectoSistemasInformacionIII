from app.domain.entities.lote_dosis import LoteDosis
from app.domain.repositories.lote_dosis_repository import LoteDosisRepository


class ConsultarStockDosis:
    """Evento 19: El administrador consulta el stock disponible de dosis."""

    def __init__(self, repo: LoteDosisRepository):
        self.repo = repo

    def ejecutar(self, punto_id: int | None = None) -> list[LoteDosis]:
        if punto_id is not None:
            return self.repo.listar_por_punto(punto_id)
        return self.repo.listar()
