from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.infrastructure.database.connection import Base


class RegistroTemperaturaModel(Base):
    __tablename__ = "registros_temperatura"

    id = Column(Integer, primary_key=True, index=True)
    punto_id = Column(Integer, ForeignKey("puntos_vacunacion.id"), nullable=False)
    vacuna_id = Column(Integer, ForeignKey("vacunas.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    temperatura_celsius = Column(Float, nullable=False)
    fecha_hora = Column(DateTime, nullable=False)
    observacion = Column(String(300), nullable=True)

    punto = relationship("PuntoVacunacionModel", back_populates="registros_temperatura")
