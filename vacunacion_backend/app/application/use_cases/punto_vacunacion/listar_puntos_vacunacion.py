from app.domain.entities.punto_vacunacion import PuntoVacunacion
from app.domain.repositories.punto_vacunacion_repository import (
    PuntoVacunacionRepository,
)


class ListarPuntosVacunacion:
    """Evento 18: El administrador consulta los puntos de vacunación."""

    def __init__(self, repo: PuntoVacunacionRepository):
        self.repo = repo

    def ejecutar(self) -> list[PuntoVacunacion]:
        return self.repo.listar()
