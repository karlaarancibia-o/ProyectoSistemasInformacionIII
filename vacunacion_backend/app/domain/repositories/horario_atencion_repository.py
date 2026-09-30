from abc import ABC, abstractmethod

from app.domain.entities.horario_atencion import HorarioAtencion


class HorarioAtencionRepository(ABC):
    @abstractmethod
    def listar(self) -> list[HorarioAtencion]: ...

    @abstractmethod
    def listar_por_punto(self, punto_id: int) -> list[HorarioAtencion]: ...

    @abstractmethod
    def obtener_por_id(self, horario_id: int) -> HorarioAtencion | None: ...

    @abstractmethod
    def crear(self, horario: HorarioAtencion) -> HorarioAtencion: ...

    @abstractmethod
    def actualizar(self, horario: HorarioAtencion) -> HorarioAtencion: ...

    @abstractmethod
    def eliminar(self, horario_id: int) -> None: ...
