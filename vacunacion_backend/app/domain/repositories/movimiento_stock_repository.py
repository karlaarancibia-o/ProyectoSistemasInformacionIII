from abc import ABC, abstractmethod

from app.domain.entities.movimiento_stock import MovimientoStock


class MovimientoStockRepository(ABC):
    @abstractmethod
    def listar(self) -> list[MovimientoStock]: ...

    @abstractmethod
    def obtener_por_id(self, movimiento_id: int) -> MovimientoStock | None: ...

    @abstractmethod
    def crear(self, movimiento: MovimientoStock) -> MovimientoStock: ...

    @abstractmethod
    def eliminar(self, movimiento_id: int) -> None: ...
