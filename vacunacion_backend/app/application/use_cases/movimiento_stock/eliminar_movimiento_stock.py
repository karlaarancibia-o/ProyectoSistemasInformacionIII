from app.application.use_cases.movimiento_stock.obtener_movimiento_stock import (
    ObtenerMovimientoStock,
)
from app.domain.exceptions import OperacionNoPermitidaError
from app.domain.repositories.movimiento_stock_repository import (
    MovimientoStockRepository,
)


class EliminarMovimientoStock:
    """Los movimientos son el registro de auditoría del inventario y el stock
    de los lotes depende de ellos: no se pueden borrar. Para corregir un error
    se registra un movimiento de ajuste en sentido contrario."""

    def __init__(self, repo: MovimientoStockRepository):
        self.repo = repo

    def ejecutar(self, movimiento_id: int) -> None:
        ObtenerMovimientoStock(self.repo).ejecutar(movimiento_id)
        raise OperacionNoPermitidaError(
            "Los movimientos de stock son registros de auditoría y no se pueden eliminar; "
            "registre un movimiento de ajuste en sentido contrario para corregirlo"
        )
