from sqlalchemy.orm import Session

from app.domain.entities.movimiento_stock import MovimientoStock
from app.domain.repositories.movimiento_stock_repository import (
    MovimientoStockRepository,
)
from app.infrastructure.database.models.movimiento_stock import MovimientoStockModel


def a_entidad(modelo: MovimientoStockModel) -> MovimientoStock:
    return MovimientoStock(
        id=modelo.id,
        lote_id=modelo.lote_id,
        punto_id=modelo.punto_id,
        usuario_id=modelo.usuario_id,
        tipo_movimiento=modelo.tipo_movimiento,
        cantidad=modelo.cantidad,
        fecha_movimiento=modelo.fecha_movimiento,
        observacion=modelo.observacion,
    )


class SqlAlchemyMovimientoStockRepository(MovimientoStockRepository):
    def __init__(self, db: Session):
        self.db = db

    def listar(self) -> list[MovimientoStock]:
        return [a_entidad(m) for m in self.db.query(MovimientoStockModel).all()]

    def obtener_por_id(self, movimiento_id: int) -> MovimientoStock | None:
        modelo = self.db.get(MovimientoStockModel, movimiento_id)
        return a_entidad(modelo) if modelo else None

    def crear(self, movimiento: MovimientoStock) -> MovimientoStock:
        modelo = MovimientoStockModel(
            lote_id=movimiento.lote_id,
            punto_id=movimiento.punto_id,
            usuario_id=movimiento.usuario_id,
            tipo_movimiento=movimiento.tipo_movimiento,
            cantidad=movimiento.cantidad,
            fecha_movimiento=movimiento.fecha_movimiento,
            observacion=movimiento.observacion,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return a_entidad(modelo)

    def eliminar(self, movimiento_id: int) -> None:
        modelo = self.db.get(MovimientoStockModel, movimiento_id)
        if modelo:
            self.db.delete(modelo)
            self.db.commit()
