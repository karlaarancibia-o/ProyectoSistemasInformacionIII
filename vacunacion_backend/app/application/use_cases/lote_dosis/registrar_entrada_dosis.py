from datetime import date, datetime

from app.domain.entities.lote_dosis import LoteDosis
from app.domain.entities.movimiento_stock import MovimientoStock
from app.domain.exceptions import (
    DatosInvalidosError,
    NoEncontradoError,
    OperacionNoPermitidaError,
)
from app.domain.repositories.lote_dosis_repository import LoteDosisRepository
from app.domain.repositories.movimiento_stock_repository import (
    MovimientoStockRepository,
)
from app.domain.repositories.vacuna_repository import VacunaRepository


class RegistrarEntradaDosis:
    """Evento 9: El responsable registra la entrada de dosis de vacunas.

    La entrada SIEMPRE ingresa al almacén central (punto_id = None): es la
    recepción del lote desde el fabricante. Para que un punto de vacunación
    tenga dosis hay que hacer después una SALIDA del central hacia el punto
    (RegistrarSalidaDosis).

    Si ya existe un lote con el mismo número (misma vacuna) en el almacén
    central se AUMENTA su stock; si no, se crea. Siempre queda un movimiento
    de entrada en la auditoría.
    """

    def __init__(
        self,
        repo: LoteDosisRepository,
        vacuna_repo: VacunaRepository,
        movimiento_repo: MovimientoStockRepository,
    ):
        self.repo = repo
        self.vacuna_repo = vacuna_repo
        self.movimiento_repo = movimiento_repo

    def ejecutar(
        self,
        vacuna_id: int,
        numero_lote: str,
        fecha_fabricacion: date,
        fecha_vencimiento: date,
        cantidad_inicial: int,
        umbral_minimo: int,
        usuario_id: int | None = None,
    ) -> LoteDosis:
        punto_id = None  # almacén central
        vacuna = self.vacuna_repo.obtener_por_id(vacuna_id)
        if not vacuna:
            raise NoEncontradoError(f"Vacuna {vacuna_id} no encontrada")
        if not vacuna.esta_activa:
            raise OperacionNoPermitidaError("La vacuna está inactiva")

        if cantidad_inicial <= 0:
            raise DatosInvalidosError("La cantidad de dosis a ingresar debe ser mayor a 0")
        hoy = date.today()
        if fecha_fabricacion > hoy:
            raise DatosInvalidosError("La fecha de fabricación no puede ser futura")
        if fecha_vencimiento < hoy:
            raise OperacionNoPermitidaError("No se puede ingresar un lote ya vencido")

        numero_lote = numero_lote.strip()
        lote = self.repo.buscar_lote(vacuna_id, numero_lote, punto_id)
        if lote:
            if (
                lote.fecha_fabricacion != fecha_fabricacion
                or lote.fecha_vencimiento != fecha_vencimiento
            ):
                raise DatosInvalidosError(
                    f"El lote {numero_lote} ya existe con otras fechas de fabricación/vencimiento"
                )
            lote.incrementar(cantidad_inicial)
            lote.cantidad_inicial += cantidad_inicial
            lote.umbral_minimo = umbral_minimo
            lote = self.repo.actualizar(lote)
        else:
            lote = self.repo.crear(
                LoteDosis(
                    vacuna_id=vacuna_id,
                    numero_lote=numero_lote,
                    fecha_fabricacion=fecha_fabricacion,
                    fecha_vencimiento=fecha_vencimiento,
                    cantidad_inicial=cantidad_inicial,
                    umbral_minimo=umbral_minimo,
                    punto_id=punto_id,
                )
            )

        self.movimiento_repo.crear(
            MovimientoStock(
                lote_id=lote.id,
                tipo_movimiento="entrada",
                cantidad=cantidad_inicial,
                fecha_movimiento=datetime.now(),
                usuario_id=usuario_id,
                punto_id=punto_id,
                observacion="Ingreso al almacén central",
            )
        )
        return lote
