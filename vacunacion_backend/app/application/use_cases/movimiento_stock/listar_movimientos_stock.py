from app.domain.entities.movimiento_stock import MovimientoStock
from app.domain.repositories.movimiento_stock_repository import (
    MovimientoStockRepository,
)


class ListarMovimientosStock:
    def __init__(self, repo: MovimientoStockRepository):
        self.repo = repo

    def ejecutar(self) -> list[MovimientoStock]:
        return self.repo.listar()
