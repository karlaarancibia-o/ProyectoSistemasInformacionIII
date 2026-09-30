from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.infrastructure.database.connection import Base


class LoteDosisModel(Base):
    __tablename__ = "lotes_dosis"

    id = Column(Integer, primary_key=True, index=True)
    vacuna_id = Column(Integer, ForeignKey("vacunas.id"), nullable=False)
    numero_lote = Column(String(50), nullable=False)
    fecha_fabricacion = Column(Date, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    cantidad_inicial = Column(Integer, nullable=False, default=0)
    cantidad_actual = Column(Integer, nullable=False, default=0)
    umbral_minimo = Column(Integer, nullable=False, default=0)
    punto_id = Column(Integer, ForeignKey("puntos_vacunacion.id"), nullable=True)

    punto = relationship("PuntoVacunacionModel", back_populates="lotes")
    registros_vacunacion = relationship("RegistroVacunacionModel", back_populates="lote")
