from dataclasses import dataclass

from app.domain.exceptions import DatosInvalidosError


@dataclass
class GrupoEdad:
    nombre: str
    edad_min: int
    edad_max: int
    prioridad: int  # 1 = máxima prioridad
    id: int | None = None
    descripcion: str | None = None

    def __post_init__(self):
        if not self.nombre.strip():
            raise DatosInvalidosError("El nombre del grupo de edad es obligatorio")
        if self.edad_min < 0 or self.edad_max < 0:
            raise DatosInvalidosError("Las edades no pueden ser negativas")
        if self.edad_max < self.edad_min:
            raise DatosInvalidosError(
                "La edad máxima no puede ser menor a la edad mínima"
            )
        if self.prioridad <= 0:
            raise DatosInvalidosError("La prioridad debe ser un valor positivo")

    def contiene_edad(self, edad: int) -> bool:
        return self.edad_min <= edad <= self.edad_max

    def se_superpone_con(self, otro: "GrupoEdad") -> bool:
        return self.edad_min <= otro.edad_max and otro.edad_min <= self.edad_max
