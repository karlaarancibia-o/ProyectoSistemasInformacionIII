from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.infrastructure.database.connection import Base


class RegistroVacunacionModel(Base):
    __tablename__ = "registros_vacunacion"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    campana_id = Column(Integer, ForeignKey("campanas.id"), nullable=False)
    punto_id = Column(Integer, ForeignKey("puntos_vacunacion.id"), nullable=False)
    lote_id = Column(Integer, ForeignKey("lotes_dosis.id"), nullable=False)
    vacuna_id = Column(Integer, ForeignKey("vacunas.id"), nullable=False)
    fecha_aplicacion = Column(Date, nullable=False)
    numero_dosis = Column(Integer, nullable=False)
    es_refuerzo = Column(Boolean, nullable=False, default=False)

    paciente = relationship("PacienteModel", back_populates="registros_vacunacion")
    campana = relationship("CampanaModel", back_populates="registros_vacunacion")
    lote = relationship("LoteDosisModel", back_populates="registros_vacunacion")
