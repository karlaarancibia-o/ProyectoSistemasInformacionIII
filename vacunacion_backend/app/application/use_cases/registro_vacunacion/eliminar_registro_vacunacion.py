from datetime import datetime

from app.domain.entities.movimiento_stock import MovimientoStock
from app.domain.exceptions import OperacionNoPermitidaError
from app.domain.repositories.lote_dosis_repository import LoteDosisRepository
from app.domain.repositories.movimiento_stock_repository import (
    MovimientoStockRepository,
)
from app.domain.repositories.registro_vacunacion_repository import (
    RegistroVacunacionRepository,
)
from app.application.use_cases.registro_vacunacion.obtener_registro_vacunacion import (
    ObtenerRegistroVacunacion,
)


class EliminarRegistroVacunacion:
    """Anula un registro de vacunación (corrección de un error de carga).

    - Solo se puede anular la última dosis del paciente para esa vacuna, para
      no dejar la secuencia de dosis incoherente.
    - La dosis vuelve al stock del lote y queda constancia en movimientos.
    """

    def __init__(
        self,
        repo: RegistroVacunacionRepository,
        lote_repo: LoteDosisRepository,
        movimiento_repo: MovimientoStockRepository,
    ):
        self.repo = repo
        self.lote_repo = lote_repo
        self.movimiento_repo = movimiento_repo

    def ejecutar(self, registro_id: int, usuario_id: int | None = None) -> None:
        registro = ObtenerRegistroVacunacion(self.repo).ejecutar(registro_id)

        posteriores = [
            r
            for r in self.repo.listar_por_paciente(registro.paciente_id)
            if r.vacuna_id == registro.vacuna_id
            and r.id != registro.id
            and (r.fecha_aplicacion, r.numero_dosis)
            > (registro.fecha_aplicacion, registro.numero_dosis)
        ]
        if posteriores:
            raise OperacionNoPermitidaError(
                "Solo se puede eliminar la última dosis registrada del paciente para esta vacuna"
            )

        lote = self.lote_repo.obtener_por_id(registro.lote_id)
        self.repo.eliminar(registro_id)
        if lote:
            lote.incrementar(1)
            self.lote_repo.actualizar(lote)
            self.movimiento_repo.crear(
                MovimientoStock(
                    lote_id=lote.id,
                    tipo_movimiento="entrada",
                    cantidad=1,
                    fecha_movimiento=datetime.now(),
                    usuario_id=usuario_id,
                    punto_id=registro.punto_id,
                    observacion=f"Anulación del registro de vacunación #{registro_id}",
                )
            )
