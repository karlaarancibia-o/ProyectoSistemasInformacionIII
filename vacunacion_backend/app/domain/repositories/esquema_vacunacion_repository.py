from abc import ABC, abstractmethod

from app.domain.entities.esquema_vacunacion import EsquemaVacunacion


class EsquemaVacunacionRepository(ABC):
    @abstractmethod
    def listar(self) -> list[EsquemaVacunacion]: ...

    @abstractmethod
    def obtener_por_id(self, esquema_id: int) -> EsquemaVacunacion | None: ...

    @abstractmethod
    def crear(self, esquema: EsquemaVacunacion) -> EsquemaVacunacion: ...

    @abstractmethod
    def actualizar(self, esquema: EsquemaVacunacion) -> EsquemaVacunacion: ...

    @abstractmethod
    def eliminar(self, esquema_id: int) -> None: ...
