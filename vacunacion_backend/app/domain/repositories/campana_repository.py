from abc import ABC, abstractmethod
from datetime import date

from app.domain.entities.campana import Campana


class CampanaRepository(ABC):
    @abstractmethod
    def listar(self) -> list[Campana]: ...

    @abstractmethod
    def listar_activas(self) -> list[Campana]: ...

    @abstractmethod
    def listar_planificadas_desde(self, fecha_inicio: date) -> list[Campana]:
        """Campañas planificadas cuya fecha_inicio ya se alcanzó (<= fecha)."""

    @abstractmethod
    def listar_activas_hasta(self, fecha_fin: date) -> list[Campana]:
        """Campañas activas cuya fecha_fin ya se alcanzó (<= fecha)."""

    @abstractmethod
    def obtener_por_id(self, campana_id: int) -> Campana | None: ...

    @abstractmethod
    def crear(self, campana: Campana) -> Campana: ...

    @abstractmethod
    def actualizar(self, campana: Campana) -> Campana: ...

    @abstractmethod
    def eliminar(self, campana_id: int) -> None: ...
