from dataclasses import dataclass, field
from datetime import date

from app.domain.exceptions import DatosInvalidosError, OperacionNoPermitidaError

ESTADOS_VALIDOS = ("planificada", "activa", "finalizada")


@dataclass
class Campana:
    nombre: str
    tipo_temporada: str  # ej. "Influenza estacional"
    fecha_inicio: date
    fecha_fin: date
    vacuna_id: int
    id: int | None = None
    descripcion: str | None = None
    grupo_edad_ids: list[int] = field(default_factory=list)
    punto_ids: list[int] = field(default_factory=list)
    estado: str = "planificada"

    def __post_init__(self):
        if not self.nombre.strip():
            raise DatosInvalidosError("El nombre de la campaña es obligatorio")
        if self.fecha_fin <= self.fecha_inicio:
            raise DatosInvalidosError(
                "La fecha de fin debe ser posterior a la fecha de inicio"
            )
        if self.estado not in ESTADOS_VALIDOS:
            raise DatosInvalidosError("Estado de campaña inválido")

    def asignar_punto(self, punto_id: int) -> None:
        if punto_id in self.punto_ids:
            raise DatosInvalidosError("El punto ya está asignado a esta campaña")
        self.punto_ids.append(punto_id)

    def quitar_punto(self, punto_id: int) -> None:
        if punto_id not in self.punto_ids:
            raise DatosInvalidosError("El punto no está asignado a esta campaña")
        self.punto_ids.remove(punto_id)

    def asignar_grupo_edad(self, grupo_edad_id: int) -> None:
        if grupo_edad_id in self.grupo_edad_ids:
            raise DatosInvalidosError(
                "El grupo de edad ya está asignado a esta campaña"
            )
        self.grupo_edad_ids.append(grupo_edad_id)

    def quitar_grupo_edad(self, grupo_edad_id: int) -> None:
        if grupo_edad_id not in self.grupo_edad_ids:
            raise DatosInvalidosError(
                "El grupo de edad no está asignado a esta campaña"
            )
        self.grupo_edad_ids.remove(grupo_edad_id)

    def activar(self, hoy: date) -> None:
        if self.estado != "planificada":
            raise OperacionNoPermitidaError("Solo una campaña planificada puede activarse")
        if hoy < self.fecha_inicio:
            raise OperacionNoPermitidaError("Aún no se alcanza la fecha de inicio")
        self.estado = "activa"

    def finalizar(self, hoy: date) -> None:
        if self.estado != "activa":
            raise OperacionNoPermitidaError("Solo una campaña activa puede finalizarse")
        if hoy < self.fecha_fin:
            raise OperacionNoPermitidaError("Aún no se alcanza la fecha de finalización")
        self.estado = "finalizada"
