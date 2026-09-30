from abc import ABC, abstractmethod

from app.domain.entities.usuario import Usuario


class UsuarioRepository(ABC):
    @abstractmethod
    def listar(self) -> list[Usuario]: ...

    @abstractmethod
    def obtener_por_id(self, usuario_id: int) -> Usuario | None: ...

    @abstractmethod
    def obtener_por_username(self, username: str) -> Usuario | None: ...

    @abstractmethod
    def crear(self, usuario: Usuario) -> Usuario: ...

    @abstractmethod
    def actualizar(self, usuario: Usuario) -> Usuario: ...

    @abstractmethod
    def contar_administradores_activos(self) -> int: ...
