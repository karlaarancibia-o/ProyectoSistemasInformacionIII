from datetime import date

from app.domain.entities.punto_vacunacion import PuntoVacunacion
from app.domain.repositories.punto_vacunacion_repository import (
    PuntoVacunacionRepository,
)
from app.domain.repositories.registro_temperatura_repository import (
    RegistroTemperaturaRepository,
)


class ObtenerPuntosPendientesRegistroTemperatura:
    """Evento 15 (temporal): Se cumple el ciclo diario de registro de
    temperaturas. Devuelve los puntos que aún no registraron su temperatura
    del día, para generar el recordatorio correspondiente."""

    def __init__(
        self,
        punto_repo: PuntoVacunacionRepository,
        temperatura_repo: RegistroTemperaturaRepository,
    ):
        self.punto_repo = punto_repo
        self.temperatura_repo = temperatura_repo

    def ejecutar(self) -> list[PuntoVacunacion]:
        hoy = date.today()
        puntos = self.punto_repo.listar()
        ids_puntos = [p.id for p in puntos if p.id is not None]
        ids_pendientes = self.temperatura_repo.puntos_sin_registro_en_fecha(
            ids_puntos, hoy
        )
        return [p for p in puntos if p.id in ids_pendientes]
