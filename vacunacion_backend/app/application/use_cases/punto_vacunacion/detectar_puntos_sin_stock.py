from datetime import date

from app.domain.entities.punto_vacunacion import PuntoVacunacion
from app.domain.repositories.lote_dosis_repository import LoteDosisRepository
from app.domain.repositories.punto_vacunacion_repository import (
    PuntoVacunacionRepository,
)


class DetectarPuntosSinStock:
    """Evento 27: El sistema detecta que un punto de vacunación no tiene
    dosis disponibles."""

    def __init__(
        self, punto_repo: PuntoVacunacionRepository, lote_repo: LoteDosisRepository
    ):
        self.punto_repo = punto_repo
        self.lote_repo = lote_repo

    def ejecutar(self) -> list[PuntoVacunacion]:
        hoy = date.today()
        sin_stock = []
        for punto in self.punto_repo.listar():
            lotes = self.lote_repo.listar_por_punto(punto.id)
            # un lote vencido no cuenta como dosis disponibles
            stock_total = sum(
                lote.cantidad_actual for lote in lotes if not lote.esta_vencido(hoy)
            )
            if stock_total == 0:
                sin_stock.append(punto)
        return sin_stock
