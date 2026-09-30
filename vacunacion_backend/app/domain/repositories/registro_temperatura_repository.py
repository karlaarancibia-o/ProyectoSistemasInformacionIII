from abc import ABC, abstractmethod
from datetime import date

from app.domain.entities.registro_temperatura import RegistroTemperatura


class RegistroTemperaturaRepository(ABC):
    @abstractmethod
    def listar(self) -> list[RegistroTemperatura]: ...

    @abstractmethod
    def listar_por_punto(self, punto_id: int) -> list[RegistroTemperatura]: ...

    @abstractmethod
    def obtener_por_id(self, registro_id: int) -> RegistroTemperatura | None: ...

    @abstractmethod
    def crear(self, registro: RegistroTemperatura) -> RegistroTemperatura: ...

    @abstractmethod
    def eliminar(self, registro_id: int) -> None: ...

    @abstractmethod
    def listar_fuera_de_rango(self) -> list[RegistroTemperatura]: ...

    @abstractmethod
    def puntos_sin_registro_en_fecha(
        self, puntos_ids: list[int], fecha: date
    ) -> list[int]:
        """IDs de puntos que aún no registraron temperatura en esa fecha."""
