from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.infrastructure.database.connection import Base
from app.infrastructure.database.models.asociaciones import (
    campana_grupo_edad,
    campana_punto_vacunacion,
)


class CampanaModel(Base):
    __tablename__ = "campanas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(String(500), nullable=True)
    tipo_temporada = Column(String(100), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    vacuna_id = Column(Integer, ForeignKey("vacunas.id"), nullable=False)
    estado = Column(String(20), nullable=False, default="planificada")

    grupos_edad = relationship(
        "GrupoEdadModel", secondary=campana_grupo_edad, back_populates="campanas"
    )
    puntos = relationship(
        "PuntoVacunacionModel", secondary=campana_punto_vacunacion, back_populates="campanas"
    )
    registros_vacunacion = relationship("RegistroVacunacionModel", back_populates="campana")
