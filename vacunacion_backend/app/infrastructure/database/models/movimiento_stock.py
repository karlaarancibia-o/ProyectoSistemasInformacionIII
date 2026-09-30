from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.infrastructure.database.connection import Base


class MovimientoStockModel(Base):
    __tablename__ = "movimientos_stock"

    id = Column(Integer, primary_key=True, index=True)
    lote_id = Column(Integer, ForeignKey("lotes_dosis.id"), nullable=False)
    punto_id = Column(Integer, ForeignKey("puntos_vacunacion.id"), nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    tipo_movimiento = Column(String(10), nullable=False)
    cantidad = Column(Integer, nullable=False)
    fecha_movimiento = Column(DateTime, nullable=False)
    observacion = Column(String(300), nullable=True)
