from abc import ABC, abstractmethod

from app.domain.entities.paciente import Paciente


class PacienteRepository(ABC):
    @abstractmethod
    def listar(self) -> list[Paciente]: ...

    @abstractmethod
    def obtener_por_id(self, paciente_id: int) -> Paciente | None: ...

    @abstractmethod
    def obtener_por_carnet(self, carnet_identidad: str) -> Paciente | None: ...

    @abstractmethod
    def crear(self, paciente: Paciente) -> Paciente: ...

    @abstractmethod
    def eliminar(self, paciente_id: int) -> None: ...
