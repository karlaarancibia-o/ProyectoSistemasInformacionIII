from datetime import date

from fastapi import APIRouter, Depends
from app.presentation.api.dependencias import requiere_administrador, requiere_logistica

from app.application.use_cases.lote_dosis.consultar_stock_dosis import ConsultarStockDosis
from app.application.use_cases.lote_dosis.detectar_lotes_vencidos import DetectarLotesVencidos
from app.application.use_cases.lote_dosis.detectar_stock_bajo import DetectarStockBajo
from app.application.use_cases.lote_dosis.eliminar_lote_dosis import EliminarLoteDosis
from app.application.use_cases.lote_dosis.listar_lotes_dosis import ListarLotesDosis
from app.application.use_cases.lote_dosis.listar_vacunas_con_stock_en_punto import ListarVacunasConStockEnPunto
from app.application.use_cases.lote_dosis.obtener_lote_dosis import ObtenerLoteDosis
from app.application.use_cases.lote_dosis.registrar_entrada_dosis import RegistrarEntradaDosis
from app.application.use_cases.lote_dosis.registrar_salida_dosis import RegistrarSalidaDosis
from app.application.use_cases.lote_dosis.revisar_inventario_periodico import RevisarInventarioPeriodico
from app.application.use_cases.registro_temperatura.detectar_temperatura_fuera_de_rango import DetectarTemperaturaFueraDeRango
from app.application.use_cases.registro_temperatura.eliminar_registro_temperatura import EliminarRegistroTemperatura
from app.application.use_cases.registro_temperatura.listar_registros_temperatura import ListarRegistrosTemperatura
from app.application.use_cases.registro_temperatura.obtener_registro_temperatura import ObtenerRegistroTemperatura
from app.application.use_cases.registro_temperatura.registrar_temperatura import RegistrarTemperatura
from app.application.use_cases.punto_vacunacion.detectar_puntos_sin_stock import DetectarPuntosSinStock
from app.application.use_cases.punto_vacunacion.obtener_puntos_pendientes_registro_temperatura import ObtenerPuntosPendientesRegistroTemperatura
from app.domain.entities.usuario import Usuario
from app.domain.repositories.lote_dosis_repository import LoteDosisRepository
from app.domain.repositories.movimiento_stock_repository import MovimientoStockRepository
from app.domain.repositories.punto_vacunacion_repository import PuntoVacunacionRepository
from app.domain.repositories.registro_temperatura_repository import RegistroTemperaturaRepository
from app.domain.repositories.vacuna_repository import VacunaRepository
from app.presentation.api.dependencias import get_lote_dosis_repository, get_movimiento_stock_repository, get_punto_vacunacion_repository, get_registro_temperatura_repository, get_vacuna_repository, obtener_usuario_actual
from app.presentation.api.schemas.lote_dosis import LoteDosisResponse, RegistrarEntradaDosisRequest, RegistrarSalidaDosisRequest, RegistrarTemperaturaRequest, RegistroTemperaturaResponse, ResultadoRevisionInventarioResponse
from app.presentation.api.schemas.punto_vacunacion import PuntoVacunacionResponse
from app.presentation.api.schemas.vacuna import VacunaResponse

router = APIRouter(prefix="/stock-dosis", tags=["Stock y Cadena de Frío"], dependencies=[Depends(obtener_usuario_actual)])


@router.post("/entradas", response_model=LoteDosisResponse, status_code=201, dependencies=[Depends(requiere_logistica)], summary="Registrar entrada")
def registrar_entrada(datos: RegistrarEntradaDosisRequest, repo: LoteDosisRepository = Depends(get_lote_dosis_repository), vacuna_repo: VacunaRepository = Depends(get_vacuna_repository), movimiento_repo: MovimientoStockRepository = Depends(get_movimiento_stock_repository), usuario: Usuario = Depends(obtener_usuario_actual)):
    """Recibe un lote (número, fechas, cantidad) en el ALMACÉN CENTRAL. No lleva punto: el lote queda con punto_id = null.
    Para que un punto pueda aplicar dosis hay que despacharlas después con `POST /stock-dosis/salidas`."""
    return RegistrarEntradaDosis(repo, vacuna_repo, movimiento_repo).ejecutar(**datos.model_dump(), usuario_id=usuario.id)


@router.post("/salidas", response_model=LoteDosisResponse, status_code=201, dependencies=[Depends(requiere_logistica)], summary="Registrar salida")
def registrar_salida(datos: RegistrarSalidaDosisRequest, repo: LoteDosisRepository = Depends(get_lote_dosis_repository), punto_repo: PuntoVacunacionRepository = Depends(get_punto_vacunacion_repository), movimiento_repo: MovimientoStockRepository = Depends(get_movimiento_stock_repository), usuario: Usuario = Depends(obtener_usuario_actual)):
    """Descuenta `cantidad` del lote del almacén central y deja ese stock en el punto de destino.
    Sin este paso el punto no tiene lote y no se puede registrar ninguna dosis aplicada allí."""
    return RegistrarSalidaDosis(repo, punto_repo, movimiento_repo).ejecutar(**datos.model_dump(), usuario_id=usuario.id)


@router.get("/", response_model=list[LoteDosisResponse])
def consultar_stock(punto_id: int | None = None, repo: LoteDosisRepository = Depends(get_lote_dosis_repository)):
    return ConsultarStockDosis(repo).ejecutar(punto_id)


@router.get("/almacen-central", response_model=list[LoteDosisResponse], summary="Stock del almacén central")
def consultar_stock_almacen_central(repo: LoteDosisRepository = Depends(get_lote_dosis_repository)):
    """Lotes que están en el almacén central (punto_id = null), pendientes de despachar a los puntos."""
    return repo.listar_por_punto(None)


@router.get("/puntos/{punto_id}/vacunas", response_model=list[VacunaResponse])
def listar_vacunas_con_stock_en_punto(punto_id: int, repo: LoteDosisRepository = Depends(get_lote_dosis_repository), vacuna_repo: VacunaRepository = Depends(get_vacuna_repository), punto_repo: PuntoVacunacionRepository = Depends(get_punto_vacunacion_repository)):
    """Vacunas con stock disponible en el punto (para el formulario de cadena de frío)."""
    return ListarVacunasConStockEnPunto(repo, vacuna_repo, punto_repo).ejecutar(punto_id)


@router.get("/lotes", response_model=list[LoteDosisResponse])
def listar_lotes(repo: LoteDosisRepository = Depends(get_lote_dosis_repository)):
    return ListarLotesDosis(repo).ejecutar()


@router.get("/lotes/{lote_id}", response_model=LoteDosisResponse)
def obtener_lote(lote_id: int, repo: LoteDosisRepository = Depends(get_lote_dosis_repository)):
    return ObtenerLoteDosis(repo).ejecutar(lote_id)


@router.delete("/lotes/{lote_id}", status_code=204, dependencies=[Depends(requiere_administrador)])
def eliminar_lote(lote_id: int, repo: LoteDosisRepository = Depends(get_lote_dosis_repository)):
    EliminarLoteDosis(repo).ejecutar(lote_id)


@router.get("/stock-bajo", response_model=list[LoteDosisResponse], dependencies=[Depends(requiere_logistica)])
def detectar_stock_bajo(repo: LoteDosisRepository = Depends(get_lote_dosis_repository)):
    return DetectarStockBajo(repo).ejecutar()


@router.get("/vencidos", response_model=list[LoteDosisResponse], dependencies=[Depends(requiere_logistica)])
def detectar_lotes_vencidos(repo: LoteDosisRepository = Depends(get_lote_dosis_repository)):
    return DetectarLotesVencidos(repo).ejecutar()


@router.get("/puntos-sin-stock", response_model=list[PuntoVacunacionResponse], dependencies=[Depends(requiere_logistica)])
def detectar_puntos_sin_stock(punto_repo: PuntoVacunacionRepository = Depends(get_punto_vacunacion_repository), lote_repo: LoteDosisRepository = Depends(get_lote_dosis_repository)):
    return DetectarPuntosSinStock(punto_repo, lote_repo).ejecutar()


@router.post("/revision-periodica", response_model=ResultadoRevisionInventarioResponse, dependencies=[Depends(requiere_logistica)])
def revisar_inventario_periodico(repo: LoteDosisRepository = Depends(get_lote_dosis_repository)):
    return RevisarInventarioPeriodico(repo).ejecutar(date.today())


@router.post("/temperaturas", response_model=RegistroTemperaturaResponse, status_code=201, dependencies=[Depends(requiere_logistica)])
def registrar_temperatura(punto_id: int, datos: RegistrarTemperaturaRequest, repo: RegistroTemperaturaRepository = Depends(get_registro_temperatura_repository), punto_repo: PuntoVacunacionRepository = Depends(get_punto_vacunacion_repository), vacuna_repo: VacunaRepository = Depends(get_vacuna_repository), lote_repo: LoteDosisRepository = Depends(get_lote_dosis_repository), usuario: Usuario = Depends(obtener_usuario_actual)):
    campos = datos.model_dump()
    campos["usuario_id"] = campos.get("usuario_id") or usuario.id  # quien registra, salvo que se indique otro
    return RegistrarTemperatura(repo, punto_repo, vacuna_repo, lote_repo).ejecutar(punto_id=punto_id, **campos)


@router.get("/temperaturas", response_model=list[RegistroTemperaturaResponse], dependencies=[Depends(requiere_logistica)])
def listar_temperaturas(punto_id: int | None = None, repo: RegistroTemperaturaRepository = Depends(get_registro_temperatura_repository)):
    return ListarRegistrosTemperatura(repo).ejecutar(punto_id)


@router.get("/temperaturas/fuera-de-rango", response_model=list[RegistroTemperaturaResponse], dependencies=[Depends(requiere_logistica)])
def detectar_temperatura_fuera_de_rango(repo: RegistroTemperaturaRepository = Depends(get_registro_temperatura_repository)):
    return DetectarTemperaturaFueraDeRango(repo).ejecutar()


@router.get("/temperaturas/puntos-pendientes", response_model=list[PuntoVacunacionResponse], dependencies=[Depends(requiere_logistica)])
def obtener_puntos_pendientes_registro_temperatura(punto_repo: PuntoVacunacionRepository = Depends(get_punto_vacunacion_repository), temperatura_repo: RegistroTemperaturaRepository = Depends(get_registro_temperatura_repository)):
    return ObtenerPuntosPendientesRegistroTemperatura(punto_repo, temperatura_repo).ejecutar()


@router.get("/temperaturas/{registro_id}", response_model=RegistroTemperaturaResponse, dependencies=[Depends(requiere_logistica)])
def obtener_temperatura(registro_id: int, repo: RegistroTemperaturaRepository = Depends(get_registro_temperatura_repository)):
    return ObtenerRegistroTemperatura(repo).ejecutar(registro_id)


@router.delete("/temperaturas/{registro_id}", status_code=204, dependencies=[Depends(requiere_administrador)])
def eliminar_temperatura(registro_id: int, repo: RegistroTemperaturaRepository = Depends(get_registro_temperatura_repository)):
    EliminarRegistroTemperatura(repo).ejecutar(registro_id)
