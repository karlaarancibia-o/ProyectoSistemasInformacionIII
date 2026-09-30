from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.infrastructure.database.connection import Base
from app.infrastructure.database.models.asociaciones import campana_grupo_edad


class GrupoEdadModel(Base):
    __tablename__ = "grupos_edad"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    edad_min = Column(Integer, nullable=False)
    edad_max = Column(Integer, nullable=False)
    prioridad = Column(Integer, nullable=False)
    descripcion = Column(String(300), nullable=True)

    campanas = relationship(
        "CampanaModel", secondary=campana_grupo_edad, back_populates="grupos_edad"
    )
    pacientes = relationship("PacienteModel", back_populates="grupo_edad")
