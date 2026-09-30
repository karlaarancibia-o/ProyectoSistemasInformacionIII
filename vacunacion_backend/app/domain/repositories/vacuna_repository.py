from abc import ABC, abstractmethod

from app.domain.entities.vacuna import Vacuna


class VacunaRepository(ABC):
    @abstractmethod
    def listar(self) -> list[Vacuna]: ...

    @abstractmethod
    def obtener_por_id(self, vacuna_id: int) -> Vacuna | None: ...

    @abstractmethod
    def crear(self, vacuna: Vacuna) -> Vacuna: ...

    @abstractmethod
    def actualizar(self, vacuna: Vacuna) -> Vacuna: ...

    @abstractmethod
    def eliminar(self, vacuna_id: int) -> None: ...
