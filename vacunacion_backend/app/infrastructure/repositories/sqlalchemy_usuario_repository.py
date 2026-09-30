from sqlalchemy.orm import Session

from app.domain.entities.usuario import Usuario
from app.domain.repositories.usuario_repository import UsuarioRepository
from app.domain.roles import ADMINISTRADOR, normalizar_rol
from app.infrastructure.database.models.usuario import UsuarioModel


def a_entidad(modelo: UsuarioModel) -> Usuario:
    return Usuario(
        id=modelo.id,
        username=modelo.username,
        password_hash=modelo.password_hash,
        # los usuarios creados antes de existir los roles tienen 'operador'/'admin'
        rol=normalizar_rol(modelo.rol),
        activo=True if modelo.activo is None else modelo.activo,
    )


class SqlAlchemyUsuarioRepository(UsuarioRepository):
    def __init__(self, db: Session):
        self.db = db

    def listar(self) -> list[Usuario]:
        modelos = self.db.query(UsuarioModel).order_by(UsuarioModel.id).all()
        return [a_entidad(m) for m in modelos]

    def obtener_por_id(self, usuario_id: int) -> Usuario | None:
        modelo = self.db.get(UsuarioModel, usuario_id)
        return a_entidad(modelo) if modelo else None

    def obtener_por_username(self, username: str) -> Usuario | None:
        modelo = self.db.query(UsuarioModel).filter(UsuarioModel.username == username).first()
        return a_entidad(modelo) if modelo else None

    def crear(self, usuario: Usuario) -> Usuario:
        modelo = UsuarioModel(
            username=usuario.username,
            password_hash=usuario.password_hash,
            rol=usuario.rol,
            activo=usuario.activo,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return a_entidad(modelo)

    def actualizar(self, usuario: Usuario) -> Usuario:
        modelo = self.db.get(UsuarioModel, usuario.id)
        modelo.password_hash = usuario.password_hash
        modelo.rol = usuario.rol
        modelo.activo = usuario.activo
        self.db.commit()
        self.db.refresh(modelo)
        return a_entidad(modelo)

    def contar_administradores_activos(self) -> int:
        # cuenta también el valor legado 'admin'
        return sum(
            1
            for m in self.db.query(UsuarioModel).all()
            if normalizar_rol(m.rol) == ADMINISTRADOR and m.activo is not False
        )
