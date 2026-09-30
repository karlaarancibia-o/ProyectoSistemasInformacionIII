from dataclasses import dataclass, field

from app.domain.exceptions import DatosInvalidosError

ESTADOS_VALIDOS = ("activa", "inactiva")


@dataclass
class Vacuna:
    """Catálogo de vacunas que pueden utilizarse en las campañas."""

    nombre: str
    fabricante: str
    tipo: str
    temperatura_minima: float
    temperatura_maxima: float
    id: int | None = None
    descripcion: str | None = None
    estado: str = "activa"
    # grupos de edad a los que está indicada. Vacío = vacuna antigua sin indicación
    # definida (no se restringe); las nuevas siempre llevan al menos uno.
    grupo_edad_ids: list[int] = field(default_factory=list)

    def __post_init__(self):
        if not self.nombre.strip():
            raise DatosInvalidosError("El nombre de la vacuna es obligatorio")
        if not self.fabricante.strip():
            raise DatosInvalidosError("El fabricante de la vacuna es obligatorio")
        if self.temperatura_maxima < self.temperatura_minima:
            raise DatosInvalidosError(
                "La temperatura máxima no puede ser menor a la mínima"
            )
        if self.estado not in ESTADOS_VALIDOS:
            raise DatosInvalidosError("El estado de la vacuna debe ser 'activa' o 'inactiva'")

    @property
    def esta_activa(self) -> bool:
        return self.estado == "activa"

    def indicada_para(self, grupo_edad_id: int) -> bool:
        """True si la vacuna puede aplicarse a ese grupo de edad."""
        return not self.grupo_edad_ids or grupo_edad_id in self.grupo_edad_ids
