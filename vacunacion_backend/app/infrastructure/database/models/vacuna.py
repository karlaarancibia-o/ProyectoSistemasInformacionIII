from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from app.infrastructure.database.connection import Base
from app.infrastructure.database.models.asociaciones import vacuna_grupo_edad


class VacunaModel(Base):
    __tablename__ = "vacunas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    fabricante = Column(String(150), nullable=False)
    tipo = Column(String(100), nullable=False)
    descripcion = Column(String(500), nullable=True)
    temperatura_minima = Column(Float, nullable=False)
    temperatura_maxima = Column(Float, nullable=False)
    estado = Column(String(20), nullable=False, default="activa")

    # grupos de edad a los que está indicada la vacuna
    grupos_edad = relationship("GrupoEdadModel", secondary=vacuna_grupo_edad)
