from app.domain.entities.movimiento_stock import MovimientoStock
from app.domain.exceptions import NoEncontradoError
from app.domain.repositories.movimiento_stock_repository import (
    MovimientoStockRepository,
)


class ObtenerMovimientoStock:
    def __init__(self, repo: MovimientoStockRepository):
        self.repo = repo

    def ejecutar(self, movimiento_id: int) -> MovimientoStock:
        movimiento = self.repo.obtener_por_id(movimiento_id)
        if not movimiento:
            raise NoEncontradoError("Movimiento de stock no encontrado")
        return movimiento
