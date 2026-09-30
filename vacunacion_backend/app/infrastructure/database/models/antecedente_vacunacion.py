from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.infrastructure.database.connection import Base


class AntecedenteVacunacionModel(Base):
    __tablename__ = "antecedentes_vacunacion"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    vacuna = Column(String(100), nullable=False)
    fecha_aplicacion = Column(Date, nullable=False)
    numero_dosis = Column(Integer, nullable=False)
    observaciones = Column(String(300), nullable=True)

    paciente = relationship("PacienteModel", back_populates="antecedentes")
