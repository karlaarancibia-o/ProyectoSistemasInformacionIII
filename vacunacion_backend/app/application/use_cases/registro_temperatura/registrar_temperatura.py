from datetime import datetime

from app.application.use_cases.lote_dosis.listar_vacunas_con_stock_en_punto import (
    vacunas_con_stock,
)
from app.domain.entities.registro_temperatura import RegistroTemperatura
from app.domain.exceptions import NoEncontradoError, OperacionNoPermitidaError
from app.domain.repositories.lote_dosis_repository import LoteDosisRepository
from app.domain.repositories.punto_vacunacion_repository import (
    PuntoVacunacionRepository,
)
from app.domain.repositories.registro_temperatura_repository import (
    RegistroTemperaturaRepository,
)
from app.domain.repositories.vacuna_repository import VacunaRepository


class RegistrarTemperatura:
    """Evento 11: El responsable registra la temperatura de almacenamiento.

    Solo se puede registrar la temperatura de una vacuna que el punto tiene
    almacenada (lote con dosis disponibles). El "fuera de rango" se evalúa
    contra el rango de temperatura de esa vacuna.
    """

    def __init__(
        self,
        repo: RegistroTemperaturaRepository,
        punto_repo: PuntoVacunacionRepository,
        vacuna_repo: VacunaRepository,
        lote_repo: LoteDosisRepository,
    ):
        self.repo = repo
        self.punto_repo = punto_repo
        self.vacuna_repo = vacuna_repo
        self.lote_repo = lote_repo

    def ejecutar(
        self,
        punto_id: int,
        vacuna_id: int,
        temperatura_celsius: float,
        fecha_hora: datetime,
        usuario_id: int | None = None,
        observacion: str | None = None,
    ) -> RegistroTemperatura:
        punto = self.punto_repo.obtener_por_id(punto_id)
        if not punto:
            raise NoEncontradoError("Punto de vacunación no encontrado")
        if punto.estado != "activo":
            raise OperacionNoPermitidaError("El punto de vacunación está inactivo")

        vacuna = self.vacuna_repo.obtener_por_id(vacuna_id)
        if not vacuna:
            raise NoEncontradoError("Vacuna no encontrada")

        disponibles = vacunas_con_stock(self.lote_repo, self.vacuna_repo, punto_id)
        if vacuna_id not in {v.id for v in disponibles}:
            raise OperacionNoPermitidaError(
                f"El punto '{punto.nombre}' no tiene stock de la vacuna '{vacuna.nombre}'; "
                "solo se registra temperatura de vacunas almacenadas en el punto"
            )

        if fecha_hora.tzinfo is not None:  # normaliza a hora local sin zona
            fecha_hora = fecha_hora.astimezone().replace(tzinfo=None)

        registro = RegistroTemperatura(
            punto_id=punto_id,
            vacuna_id=vacuna_id,
            temperatura_celsius=temperatura_celsius,
            fecha_hora=fecha_hora,
            usuario_id=usuario_id,
            observacion=observacion,
            rango_minimo=vacuna.temperatura_minima,
            rango_maximo=vacuna.temperatura_maxima,
        )
        return self.repo.crear(registro)
