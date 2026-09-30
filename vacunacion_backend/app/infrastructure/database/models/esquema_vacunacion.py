from sqlalchemy import Boolean, Column, ForeignKey, Integer

from app.infrastructure.database.connection import Base


class EsquemaVacunacionModel(Base):
    __tablename__ = "esquemas_vacunacion"

    id = Column(Integer, primary_key=True, index=True)
    vacuna_id = Column(Integer, ForeignKey("vacunas.id"), nullable=False)
    grupo_edad_id = Column(Integer, ForeignKey("grupos_edad.id"), nullable=False)
    cantidad_dosis = Column(Integer, nullable=False)
    dias_entre_dosis = Column(Integer, nullable=False)
    requiere_refuerzo = Column(Boolean, nullable=False, default=False)
    meses_refuerzo = Column(Integer, nullable=True)
