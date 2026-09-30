from dataclasses import dataclass, field

from app.domain.exceptions import DatosInvalidosError

ESTADOS_VALIDOS = ("activo", "inactivo")


@dataclass
class PuntoVacunacion:
    nombre: str
    direccion: str
    capacidad: int
    id: int | None = None
    telefono: str | None = None
    estado: str = "activo"
    campana_ids: list[int] = field(default_factory=list)

    def __post_init__(self):
        if not self.nombre.strip():
            raise DatosInvalidosError("El nombre del punto de vacunación es obligatorio")
        if not self.direccion.strip():
            raise DatosInvalidosError("La dirección del punto de vacunación es obligatoria")
        if self.capacidad <= 0:
            raise DatosInvalidosError("La capacidad debe ser un valor positivo")
        if self.estado not in ESTADOS_VALIDOS:
            raise DatosInvalidosError("Estado de punto de vacunación inválido")
