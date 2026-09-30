from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.infrastructure.database.connection import Base
from app.infrastructure.database.models.asociaciones import campana_punto_vacunacion


class PuntoVacunacionModel(Base):
    __tablename__ = "puntos_vacunacion"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    direccion = Column(String(250), nullable=False)
    telefono = Column(String(30), nullable=True)
    capacidad = Column(Integer, nullable=False)
    estado = Column(String(20), nullable=False, default="activo")

    campanas = relationship(
        "CampanaModel", secondary=campana_punto_vacunacion, back_populates="puntos"
    )
    horarios = relationship("HorarioAtencionModel", back_populates="punto")
    lotes = relationship("LoteDosisModel", back_populates="punto")
    registros_temperatura = relationship("RegistroTemperaturaModel", back_populates="punto")
