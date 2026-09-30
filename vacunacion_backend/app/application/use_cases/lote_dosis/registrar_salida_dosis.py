from datetime import date, datetime

from app.domain.entities.lote_dosis import LoteDosis
from app.domain.entities.movimiento_stock import MovimientoStock
from app.domain.exceptions import NoEncontradoError, OperacionNoPermitidaError
from app.domain.repositories.lote_dosis_repository import LoteDosisRepository
from app.domain.repositories.movimiento_stock_repository import (
    MovimientoStockRepository,
)
from app.domain.repositories.punto_vacunacion_repository import (
    PuntoVacunacionRepository,
)


class RegistrarSalidaDosis:
    """Evento 10: El responsable despacha dosis del almacén central hacia un
    punto de vacunación.

    Descuenta del lote del almacén central y suma al lote del punto (si el
    punto ya tiene ese lote se incrementa, si no se crea). Deja un movimiento
    de salida en el origen y uno de entrada en el destino.
    """

    def __init__(
        self,
        repo: LoteDosisRepository,
        punto_repo: PuntoVacunacionRepository,
        movimiento_repo: MovimientoStockRepository,
    ):
        self.repo = repo
        self.punto_repo = punto_repo
        self.movimiento_repo = movimiento_repo

    def ejecutar(
        self,
        lote_id: int,
        punto_id: int,
        cantidad: int,
        usuario_id: int | None = None,
    ) -> LoteDosis:
        lote_origen = self.repo.obtener_por_id(lote_id)
        if not lote_origen:
            raise NoEncontradoError("Lote de dosis no encontrado")
        if lote_origen.punto_id is not None:
            raise OperacionNoPermitidaError(
                "Solo se pueden despachar dosis desde el almacén central"
            )
        if lote_origen.esta_vencido(date.today()):
            raise OperacionNoPermitidaError("No se pueden despachar dosis de un lote vencido")

        punto = self.punto_repo.obtener_por_id(punto_id)
        if not punto:
            raise NoEncontradoError("Punto de vacunación no encontrado")
        if punto.estado != "activo":
            raise OperacionNoPermitidaError("El punto de vacunación está inactivo")

        lote_origen.descontar(cantidad)  # valida cantidad > 0 y stock suficiente

        lote_destino = self.repo.buscar_lote(
            lote_origen.vacuna_id, lote_origen.numero_lote, punto_id
        )
        if lote_destino:
            lote_destino.incrementar(cantidad)
            lote_destino.cantidad_inicial += cantidad
            lote_destino = self.repo.actualizar(lote_destino)
        else:
            lote_destino = self.repo.crear(
                LoteDosis(
                    vacuna_id=lote_origen.vacuna_id,
                    numero_lote=lote_origen.numero_lote,
                    fecha_fabricacion=lote_origen.fecha_fabricacion,
                    fecha_vencimiento=lote_origen.fecha_vencimiento,
                    cantidad_inicial=cantidad,
                    umbral_minimo=lote_origen.umbral_minimo,
                    punto_id=punto_id,
                )
            )
        self.repo.actualizar(lote_origen)

        ahora = datetime.now()
        self.movimiento_repo.crear(
            MovimientoStock(
                lote_id=lote_origen.id,
                tipo_movimiento="salida",
                cantidad=cantidad,
                fecha_movimiento=ahora,
                usuario_id=usuario_id,
                punto_id=punto_id,
                observacion=f"Despacho del almacén central al punto {punto.nombre}",
            )
        )
        self.movimiento_repo.crear(
            MovimientoStock(
                lote_id=lote_destino.id,
                tipo_movimiento="entrada",
                cantidad=cantidad,
                fecha_movimiento=ahora,
                usuario_id=usuario_id,
                punto_id=punto_id,
                observacion="Recepción desde el almacén central",
            )
        )
        return lote_destino
