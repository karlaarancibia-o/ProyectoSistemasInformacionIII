from app.domain.entities.punto_vacunacion import PuntoVacunacion
from app.domain.exceptions import NoEncontradoError
from app.domain.repositories.punto_vacunacion_repository import (
    PuntoVacunacionRepository,
)


class ObtenerPuntoVacunacion:
    def __init__(self, repo: PuntoVacunacionRepository):
        self.repo = repo

    def ejecutar(self, punto_id: int) -> PuntoVacunacion:
        punto = self.repo.obtener_por_id(punto_id)
        if not punto:
            raise NoEncontradoError("Punto de vacunación no encontrado")
        return punto
