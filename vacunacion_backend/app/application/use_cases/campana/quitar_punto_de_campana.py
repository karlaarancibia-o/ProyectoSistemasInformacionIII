from app.domain.entities.campana import Campana
from app.domain.exceptions import NoEncontradoError
from app.domain.repositories.campana_repository import CampanaRepository
from app.domain.repositories.punto_vacunacion_repository import (
    PuntoVacunacionRepository,
)


class QuitarPuntoDeCampana:
    """Desasocia un punto de vacunación de una campaña."""

    def __init__(
        self, campana_repo: CampanaRepository, punto_repo: PuntoVacunacionRepository
    ):
        self.campana_repo = campana_repo
        self.punto_repo = punto_repo

    def ejecutar(self, campana_id: int, punto_id: int) -> Campana:
        campana = self.campana_repo.obtener_por_id(campana_id)
        if not campana:
            raise NoEncontradoError("Campaña no encontrada")

        punto = self.punto_repo.obtener_por_id(punto_id)
        if not punto:
            raise NoEncontradoError("Punto de vacunación no encontrado")

        campana.quitar_punto(punto_id)  # valida que estuviera asignado
        if punto_id in punto.campana_ids:
            punto.campana_ids.remove(punto_id)

        self.punto_repo.actualizar(punto)
        return self.campana_repo.actualizar(campana)
