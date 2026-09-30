from datetime import date, datetime

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
from app.domain.repositories.punto_vacunacion_repository import (
    PuntoVacunacionRepository,
)


class RegistrarMovimientoStock:
    """Ajuste manual de inventario sobre un lote (p. ej. merma, descarte,
    corrección de conteo).

    El movimiento SÍ modifica el stock del lote: una entrada suma y una
    salida resta. Los movimientos que generan las entradas, salidas y dosis
    aplicadas se crean automáticamente.

    Para no saltarse el flujo almacén central -> punto, un ajuste de ENTRADA
    solo se admite sobre lotes del almacén central; un punto solo recibe
    dosis mediante una salida del central (POST /stock-dosis/salidas).
    """

    def __init__(
        self,
        repo: MovimientoStockRepository,
        lote_repo: LoteDosisRepository,
        punto_repo: PuntoVacunacionRepository,
    ):
        self.repo = repo
        self.lote_repo = lote_repo
        self.punto_repo = punto_repo

    def ejecutar(
        self,
        lote_id: int,
        tipo_movimiento: str,
        cantidad: int,
        usuario_id: int | None = None,
        punto_id: int | None = None,
        observacion: str | None = None,
        fecha_movimiento: datetime | None = None,
    ) -> MovimientoStock:
        lote = self.lote_repo.obtener_por_id(lote_id)
        if not lote:
            raise NoEncontradoError("Lote de dosis no encontrado")

        if punto_id is not None:
            if not self.punto_repo.obtener_por_id(punto_id):
                raise NoEncontradoError("Punto de vacunación no encontrado")
            if punto_id != lote.punto_id:
                raise DatosInvalidosError(
                    "El punto indicado no coincide con la ubicación actual del lote"
                )
        punto_id = lote.punto_id  # el movimiento ocurre donde está el lote

        if fecha_movimiento and fecha_movimiento.tzinfo:
            fecha_movimiento = fecha_movimiento.astimezone().replace(tzinfo=None)
        if fecha_movimiento and fecha_movimiento > datetime.now():
            raise DatosInvalidosError("La fecha del movimiento no puede ser futura")

        movimiento = MovimientoStock(  # valida tipo y cantidad
            lote_id=lote_id,
            tipo_movimiento=tipo_movimiento,
            cantidad=cantidad,
            usuario_id=usuario_id,
            punto_id=punto_id,
            observacion=observacion,
            fecha_movimiento=fecha_movimiento or datetime.now(),
        )

        if tipo_movimiento == "entrada":
            if lote.punto_id is not None:
                raise OperacionNoPermitidaError(
                    "No se puede sumar stock directamente a un lote de un punto de "
                    "vacunación: las dosis llegan al punto con una salida desde el "
                    "almacén central (POST /stock-dosis/salidas)"
                )
            if lote.esta_vencido(date.today()):
                raise OperacionNoPermitidaError("No se puede ingresar stock a un lote vencido")
            lote.incrementar(cantidad)
            lote.cantidad_inicial += cantidad
        else:
            lote.descontar(cantidad)  # valida stock suficiente
        self.lote_repo.actualizar(lote)
        return self.repo.crear(movimiento)
