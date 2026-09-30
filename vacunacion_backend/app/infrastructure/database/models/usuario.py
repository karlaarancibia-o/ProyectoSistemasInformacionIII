from sqlalchemy import Boolean, Column, Integer, String

from app.infrastructure.database.connection import Base


class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    rol = Column(String(20), default="personal_salud")
    activo = Column(Boolean, default=True)
