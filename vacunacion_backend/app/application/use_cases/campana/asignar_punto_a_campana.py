from app.domain.entities.campana import Campana
from app.domain.exceptions import NoEncontradoError, OperacionNoPermitidaError
from app.domain.repositories.campana_repository import CampanaRepository
from app.domain.repositories.punto_vacunacion_repository import (
    PuntoVacunacionRepository,
)


class AsignarPuntoACampana:
    """Evento 4: El administrador asigna un punto de vacunación a una
    campaña."""

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
        if punto.estado != "activo":
            raise OperacionNoPermitidaError("El punto de vacunación está inactivo")

        campana.asignar_punto(punto_id)  # valida duplicados
        punto.campana_ids.append(campana_id)

        self.punto_repo.actualizar(punto)
        return self.campana_repo.actualizar(campana)
