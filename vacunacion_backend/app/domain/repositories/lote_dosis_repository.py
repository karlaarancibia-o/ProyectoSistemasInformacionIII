from abc import ABC, abstractmethod
from datetime import date

from app.domain.entities.lote_dosis import LoteDosis


class LoteDosisRepository(ABC):
    @abstractmethod
    def listar(self) -> list[LoteDosis]: ...

    @abstractmethod
    def listar_por_punto(self, punto_id: int | None) -> list[LoteDosis]:
        """punto_id=None devuelve los lotes del almacén central."""

    @abstractmethod
    def obtener_por_id(self, lote_id: int) -> LoteDosis | None: ...

    @abstractmethod
    def buscar_lote(
        self, vacuna_id: int, numero_lote: str, punto_id: int | None
    ) -> LoteDosis | None:
        """Lote con ese número para esa vacuna en esa ubicación
        (punto_id=None = almacén central)."""

    @abstractmethod
    def crear(self, lote: LoteDosis) -> LoteDosis: ...

    @abstractmethod
    def actualizar(self, lote: LoteDosis) -> LoteDosis: ...

    @abstractmethod
    def eliminar(self, lote_id: int) -> None: ...

    @abstractmethod
    def listar_con_stock_bajo(self) -> list[LoteDosis]: ...

    @abstractmethod
    def listar_vencidos(self, hoy: date) -> list[LoteDosis]: ...
