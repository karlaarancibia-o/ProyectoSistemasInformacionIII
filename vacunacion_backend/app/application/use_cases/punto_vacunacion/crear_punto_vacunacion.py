from app.domain.entities.punto_vacunacion import PuntoVacunacion
from app.domain.repositories.punto_vacunacion_repository import (
    PuntoVacunacionRepository,
)


class CrearPuntoVacunacion:
    """Evento 3: El administrador registra un nuevo punto de vacunación."""

    def __init__(self, repo: PuntoVacunacionRepository):
        self.repo = repo

    def ejecutar(
        self,
        nombre: str,
        direccion: str,
        capacidad: int,
        telefono: str | None = None,
        estado: str = "activo",
    ) -> PuntoVacunacion:
        punto = PuntoVacunacion(
            nombre=nombre,
            direccion=direccion,
            capacidad=capacidad,
            telefono=telefono,
            estado=estado,
        )
        return self.repo.crear(punto)
