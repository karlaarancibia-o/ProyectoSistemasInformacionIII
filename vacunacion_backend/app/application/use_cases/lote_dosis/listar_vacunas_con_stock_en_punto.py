from datetime import date

from app.domain.entities.vacuna import Vacuna
from app.domain.exceptions import NoEncontradoError
from app.domain.repositories.lote_dosis_repository import LoteDosisRepository
from app.domain.repositories.punto_vacunacion_repository import (
    PuntoVacunacionRepository,
)
from app.domain.repositories.vacuna_repository import VacunaRepository


def vacunas_con_stock(
    lote_repo: LoteDosisRepository, vacuna_repo: VacunaRepository, punto_id: int
) -> list[Vacuna]:
    """Vacunas que el punto tiene realmente disponibles (lotes no vencidos
    con dosis)."""
    hoy = date.today()
    ids = {
        lote.vacuna_id
        for lote in lote_repo.listar_por_punto(punto_id)
        if lote.cantidad_actual > 0 and not lote.esta_vencido(hoy)
    }
    return [v for v in vacuna_repo.listar() if v.id in ids]


class ListarVacunasConStockEnPunto:
    """Para el formulario de cadena de frío: al elegir un punto solo deben
    ofrecerse las vacunas que ese punto tiene almacenadas."""

    def __init__(
        self,
        lote_repo: LoteDosisRepository,
        vacuna_repo: VacunaRepository,
        punto_repo: PuntoVacunacionRepository,
    ):
        self.lote_repo = lote_repo
        self.vacuna_repo = vacuna_repo
        self.punto_repo = punto_repo

    def ejecutar(self, punto_id: int) -> list[Vacuna]:
        if not self.punto_repo.obtener_por_id(punto_id):
            raise NoEncontradoError("Punto de vacunación no encontrado")
        return vacunas_con_stock(self.lote_repo, self.vacuna_repo, punto_id)
