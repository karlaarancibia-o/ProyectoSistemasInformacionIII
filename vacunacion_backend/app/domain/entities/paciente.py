from dataclasses import dataclass
from datetime import date

from app.domain.exceptions import DatosInvalidosError

SEXOS_VALIDOS = ("M", "F")


@dataclass
class Paciente:
    nombres: str
    apellidos: str
    carnet_identidad: str
    fecha_nacimiento: date
    sexo: str
    id: int | None = None
    telefono: str | None = None
    direccion: str | None = None
    grupo_edad_id: int | None = None

    def __post_init__(self):
        if not self.nombres.strip():
            raise DatosInvalidosError("Los nombres del paciente son obligatorios")
        if not self.apellidos.strip():
            raise DatosInvalidosError("Los apellidos del paciente son obligatorios")
        if not self.carnet_identidad.strip():
            raise DatosInvalidosError("El carnet de identidad es obligatorio")
        if self.fecha_nacimiento > date.today():
            raise DatosInvalidosError("La fecha de nacimiento no puede ser futura")
        if self.sexo not in SEXOS_VALIDOS:
            raise DatosInvalidosError("El sexo debe ser 'M' o 'F'")
