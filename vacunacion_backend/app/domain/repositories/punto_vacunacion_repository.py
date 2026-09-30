from abc import ABC, abstractmethod

from app.domain.entities.punto_vacunacion import PuntoVacunacion


class PuntoVacunacionRepository(ABC):
    @abstractmethod
    def listar(self) -> list[PuntoVacunacion]: ...

    @abstractmethod
    def obtener_por_id(self, punto_id: int) -> PuntoVacunacion | None: ...

    @abstractmethod
    def crear(self, punto: PuntoVacunacion) -> PuntoVacunacion: ...

    @abstractmethod
    def actualizar(self, punto: PuntoVacunacion) -> PuntoVacunacion: ...

    @abstractmethod
    def eliminar(self, punto_id: int) -> None: ...
