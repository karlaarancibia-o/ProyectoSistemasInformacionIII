from abc import ABC, abstractmethod

from app.domain.entities.antecedente_vacunacion import AntecedenteVacunacion


class AntecedenteVacunacionRepository(ABC):
    @abstractmethod
    def listar(self) -> list[AntecedenteVacunacion]: ...

    @abstractmethod
    def listar_por_paciente(self, paciente_id: int) -> list[AntecedenteVacunacion]: ...

    @abstractmethod
    def obtener_por_id(self, antecedente_id: int) -> AntecedenteVacunacion | None: ...

    @abstractmethod
    def crear(self, antecedente: AntecedenteVacunacion) -> AntecedenteVacunacion: ...

    @abstractmethod
    def eliminar(self, antecedente_id: int) -> None: ...
