from dataclasses import dataclass

from app.domain.entities.lote_dosis import LoteDosis
from app.domain.repositories.lote_dosis_repository import LoteDosisRepository


@dataclass
class ResultadoRevisionInventario:
    lotes_con_stock_bajo: list[LoteDosis]
    lotes_vencidos: list[LoteDosis]


class RevisarInventarioPeriodico:
    """Evento 14 (temporal): Se cumple el ciclo de revisión periódica de
    inventario. Agrupa las alertas de stock bajo (evento 23) y lotes
    vencidos (evento 16) en una sola corrida."""

    def __init__(self, repo: LoteDosisRepository):
        self.repo = repo

    def ejecutar(self, hoy) -> ResultadoRevisionInventario:
        return ResultadoRevisionInventario(
            lotes_con_stock_bajo=self.repo.listar_con_stock_bajo(),
            lotes_vencidos=self.repo.listar_vencidos(hoy),
        )
