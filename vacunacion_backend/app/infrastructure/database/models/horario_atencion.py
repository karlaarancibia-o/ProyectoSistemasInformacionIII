from sqlalchemy import Column, ForeignKey, Integer, Time
from sqlalchemy.orm import relationship

from app.infrastructure.database.connection import Base


class HorarioAtencionModel(Base):
    __tablename__ = "horarios_atencion"

    id = Column(Integer, primary_key=True, index=True)
    punto_id = Column(Integer, ForeignKey("puntos_vacunacion.id"), nullable=False)
    dia_semana = Column(Integer, nullable=False)  # 0=lunes .. 6=domingo
    hora_apertura = Column(Time, nullable=False)
    hora_cierre = Column(Time, nullable=False)

    punto = relationship("PuntoVacunacionModel", back_populates="horarios")
