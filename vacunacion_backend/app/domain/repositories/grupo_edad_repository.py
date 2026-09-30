from abc import ABC, abstractmethod

from app.domain.entities.grupo_edad import GrupoEdad


class GrupoEdadRepository(ABC):
    @abstractmethod
    def listar(self) -> list[GrupoEdad]: ...

    @abstractmethod
    def obtener_por_id(self, grupo_id: int) -> GrupoEdad | None: ...

    @abstractmethod
    def crear(self, grupo: GrupoEdad) -> GrupoEdad: ...

    @abstractmethod
    def actualizar(self, grupo: GrupoEdad) -> GrupoEdad: ...

    @abstractmethod
    def eliminar(self, grupo_id: int) -> None: ...
