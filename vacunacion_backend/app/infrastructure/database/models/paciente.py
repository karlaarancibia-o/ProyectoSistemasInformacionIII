from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.infrastructure.database.connection import Base


class PacienteModel(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nombres = Column(String(150), nullable=False)
    apellidos = Column(String(150), nullable=False)
    carnet_identidad = Column(String(30), unique=True, nullable=False, index=True)
    fecha_nacimiento = Column(Date, nullable=False)
    sexo = Column(String(1), nullable=False)
    telefono = Column(String(30), nullable=True)
    direccion = Column(String(250), nullable=True)
    grupo_edad_id = Column(Integer, ForeignKey("grupos_edad.id"), nullable=True)

    grupo_edad = relationship("GrupoEdadModel", back_populates="pacientes")
    antecedentes = relationship("AntecedenteVacunacionModel", back_populates="paciente")
    registros_vacunacion = relationship("RegistroVacunacionModel", back_populates="paciente")
