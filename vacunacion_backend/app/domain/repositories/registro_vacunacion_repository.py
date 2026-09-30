from abc import ABC, abstractmethod

from app.domain.entities.registro_vacunacion import RegistroVacunacion


class RegistroVacunacionRepository(ABC):
    @abstractmethod
    def listar_por_paciente(self, paciente_id: int) -> list[RegistroVacunacion]: ...

    @abstractmethod
    def listar_por_campana(self, campana_id: int) -> list[RegistroVacunacion]: ...

    @abstractmethod
    def crear(self, registro: RegistroVacunacion) -> RegistroVacunacion: ...

    @abstractmethod
    def listar_todos(self) -> list[RegistroVacunacion]: ...

    @abstractmethod
    def obtener_por_id(self, registro_id: int) -> RegistroVacunacion | None: ...

    @abstractmethod
    def eliminar(self, registro_id: int) -> None: ...
