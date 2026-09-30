from fastapi import APIRouter, Depends
from app.presentation.api.dependencias import requiere_administrador, requiere_logistica

from app.application.use_cases.movimiento_stock.eliminar_movimiento_stock import EliminarMovimientoStock
from app.application.use_cases.movimiento_stock.listar_movimientos_stock import ListarMovimientosStock
from app.application.use_cases.movimiento_stock.obtener_movimiento_stock import ObtenerMovimientoStock
from app.application.use_cases.movimiento_stock.registrar_movimiento_stock import RegistrarMovimientoStock
from app.domain.entities.usuario import Usuario
from app.domain.repositories.lote_dosis_repository import LoteDosisRepository
from app.domain.repositories.movimiento_stock_repository import MovimientoStockRepository
from app.domain.repositories.punto_vacunacion_repository import PuntoVacunacionRepository
from app.presentation.api.dependencias import get_lote_dosis_repository, get_movimiento_stock_repository, get_punto_vacunacion_repository, obtener_usuario_actual
from app.presentation.api.schemas.movimiento_stock import MovimientoStockCreate, MovimientoStockResponse

router = APIRouter(prefix="/movimientos-stock", tags=["Movimientos de Stock"], dependencies=[Depends(obtener_usuario_actual)])


@router.post("/", response_model=MovimientoStockResponse, status_code=201, dependencies=[Depends(requiere_logistica)], summary="Ajuste manual de stock (merma, descarte, corrección)")
def registrar(
    datos: MovimientoStockCreate,
    repo: MovimientoStockRepository = Depends(get_movimiento_stock_repository),
    lote_repo: LoteDosisRepository = Depends(get_lote_dosis_repository),
    punto_repo: PuntoVacunacionRepository = Depends(get_punto_vacunacion_repository),
    usuario: Usuario = Depends(obtener_usuario_actual),
):
    """Ajuste manual sobre un lote existente: la salida resta (merma/descarte) y la entrada suma (solo lotes del almacén central).
    NO es la forma de recibir lotes ni de despachar a puntos: para eso usar `/stock-dosis/entradas` y `/stock-dosis/salidas`."""
    campos = datos.model_dump()
    campos["usuario_id"] = campos.get("usuario_id") or usuario.id
    return RegistrarMovimientoStock(repo, lote_repo, punto_repo).ejecutar(**campos)


@router.get("/", response_model=list[MovimientoStockResponse], dependencies=[Depends(requiere_logistica)], summary="Historial (auditoría) de movimientos")
def listar(repo: MovimientoStockRepository = Depends(get_movimiento_stock_repository)):
    return ListarMovimientosStock(repo).ejecutar()


@router.get("/{movimiento_id}", response_model=MovimientoStockResponse, dependencies=[Depends(requiere_logistica)])
def obtener(movimiento_id: int, repo: MovimientoStockRepository = Depends(get_movimiento_stock_repository)):
    return ObtenerMovimientoStock(repo).ejecutar(movimiento_id)


@router.delete("/{movimiento_id}", status_code=204, dependencies=[Depends(requiere_administrador)])
def eliminar(movimiento_id: int, repo: MovimientoStockRepository = Depends(get_movimiento_stock_repository)):
    EliminarMovimientoStock(repo).ejecutar(movimiento_id)
