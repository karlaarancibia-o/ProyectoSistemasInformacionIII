from datetime import date, datetime

from app.application.services.esquema_paciente import ServicioEsquemaPaciente
from app.domain.entities.movimiento_stock import MovimientoStock
from app.domain.entities.registro_vacunacion import RegistroVacunacion
from app.domain.esquema_vacunacion import determinar_proxima_dosis
from app.domain.exceptions import (
    DatosInvalidosError,
    NoEncontradoError,
    OperacionNoPermitidaError,
)
from app.domain.reglas_edad import calcular_edad
from app.domain.repositories.campana_repository import CampanaRepository
from app.domain.repositories.lote_dosis_repository import LoteDosisRepository
from app.domain.repositories.movimiento_stock_repository import (
    MovimientoStockRepository,
)
from app.domain.repositories.paciente_repository import PacienteRepository
from app.domain.repositories.punto_vacunacion_repository import (
    PuntoVacunacionRepository,
)
from app.domain.repositories.registro_vacunacion_repository import (
    RegistroVacunacionRepository,
)


class RegistrarDosisAplicada:
    """Evento 8: El personal de salud registra una dosis aplicada.

    El sistema decide el número de dosis y si es refuerzo a partir del
    esquema de vacunación (vacuna + grupo de edad del paciente) y de lo que
    el paciente ya recibió. Si el cliente envía esos datos, se comprueba que
    coincidan con lo que corresponde.

    Validaciones: paciente; campaña activa y vigente en la fecha; punto activo
    y asignado a la campaña; el punto debe tener dosis de la vacuna de la
    campaña (recibidas por salida del almacén central); lote del punto, de la vacuna de la campaña, no
    vencido y con stock; paciente dentro de los grupos de edad de la campaña;
    esquema existente; intervalo mínimo entre dosis; esquema no completo.
    Luego descuenta 1 dosis del lote y deja constancia en movimientos de stock.
    """

    def __init__(
        self,
        registro_repo: RegistroVacunacionRepository,
        paciente_repo: PacienteRepository,
        campana_repo: CampanaRepository,
        lote_repo: LoteDosisRepository,
        punto_repo: PuntoVacunacionRepository,
        movimiento_repo: MovimientoStockRepository,
        servicio_esquema: ServicioEsquemaPaciente,
    ):
        self.registro_repo = registro_repo
        self.paciente_repo = paciente_repo
        self.campana_repo = campana_repo
        self.lote_repo = lote_repo
        self.punto_repo = punto_repo
        self.movimiento_repo = movimiento_repo
        self.servicio_esquema = servicio_esquema

    def ejecutar(
        self,
        paciente_id: int,
        campana_id: int,
        punto_id: int,
        lote_id: int,
        fecha_aplicacion: date,
        numero_dosis: int | None = None,
        es_refuerzo: bool | None = None,
        usuario_id: int | None = None,
    ) -> RegistroVacunacion:
        if fecha_aplicacion > date.today():
            raise DatosInvalidosError("La fecha de aplicación no puede ser futura")

        paciente = self.paciente_repo.obtener_por_id(paciente_id)
        if not paciente:
            raise NoEncontradoError("Paciente no encontrado")
        if fecha_aplicacion < paciente.fecha_nacimiento:
            raise DatosInvalidosError(
                "La fecha de aplicación es anterior a la fecha de nacimiento del paciente"
            )

        # ---- campaña ----
        campana = self.campana_repo.obtener_por_id(campana_id)
        if not campana:
            raise NoEncontradoError("Campaña no encontrada")
        if campana.estado != "activa":
            raise OperacionNoPermitidaError(
                "Solo se pueden aplicar dosis en campañas activas"
            )
        if not (campana.fecha_inicio <= fecha_aplicacion <= campana.fecha_fin):
            raise OperacionNoPermitidaError(
                "La fecha de aplicación está fuera del período de la campaña "
                f"({campana.fecha_inicio} a {campana.fecha_fin})"
            )

        # ---- punto ----
        punto = self.punto_repo.obtener_por_id(punto_id)
        if not punto:
            raise NoEncontradoError("Punto de vacunación no encontrado")
        if punto.estado != "activo":
            raise OperacionNoPermitidaError("El punto de vacunación está inactivo")
        if punto_id not in campana.punto_ids:
            raise OperacionNoPermitidaError(
                "El punto de vacunación no está asignado a esta campaña"
            )

        # ---- stock del punto (sin salida del central no hay dosis) ----
        disponibles = [
            l
            for l in self.lote_repo.listar_por_punto(punto_id)
            if l.vacuna_id == campana.vacuna_id
            and l.cantidad_actual > 0
            and not l.esta_vencido(fecha_aplicacion)
        ]
        if not disponibles:
            raise OperacionNoPermitidaError(
                f"El punto '{punto.nombre}' no tiene dosis disponibles de la vacuna de "
                "esta campaña. Primero se deben despachar dosis desde el almacén central "
                "(POST /stock-dosis/salidas)"
            )

        # ---- lote ----
        lote = self.lote_repo.obtener_por_id(lote_id)
        if not lote:
            raise NoEncontradoError("Lote de dosis no encontrado")
        if lote.punto_id is None:
            raise OperacionNoPermitidaError(
                "El lote seleccionado está en el almacén central: no se puede aplicar "
                "desde ahí. Despáchelo primero al punto de vacunación"
            )
        if lote.punto_id != punto_id:
            raise OperacionNoPermitidaError(
                "El lote seleccionado no pertenece a este punto de vacunación"
            )
        if lote.vacuna_id != campana.vacuna_id:
            raise OperacionNoPermitidaError(
                "El lote seleccionado no corresponde a la vacuna de esta campaña"
            )
        if lote.esta_vencido(fecha_aplicacion):
            raise OperacionNoPermitidaError(
                f"El lote {lote.numero_lote} está vencido a la fecha de aplicación"
            )
        if fecha_aplicacion < lote.fecha_fabricacion:
            raise DatosInvalidosError(
                "La fecha de aplicación es anterior a la fecha de fabricación del lote"
            )
        if lote.cantidad_actual <= 0:
            raise OperacionNoPermitidaError("El lote no tiene dosis disponibles")

        # ---- grupo de edad y esquema ----
        edad = calcular_edad(paciente.fecha_nacimiento, fecha_aplicacion)
        grupos = self.servicio_esquema.grupos_para_edad(edad)
        if not grupos:
            raise OperacionNoPermitidaError(
                f"No hay ningún grupo de edad registrado que incluya la edad del paciente ({edad} años)"
            )
        if campana.grupo_edad_ids:
            grupos = [g for g in grupos if g.id in campana.grupo_edad_ids]
            if not grupos:
                raise OperacionNoPermitidaError(
                    f"El paciente ({edad} años) no pertenece a los grupos de edad de esta campaña"
                )

        nombre_vacuna, grupos = self.servicio_esquema.grupos_indicados(lote.vacuna_id, grupos)
        if not grupos:
            raise OperacionNoPermitidaError(
                f"La vacuna '{nombre_vacuna}' no está indicada para el grupo de edad del paciente ({edad} años)"
            )

        regla = self.servicio_esquema.regla_para(lote.vacuna_id, grupos)
        if regla is None:
            raise OperacionNoPermitidaError(
                "No existe un esquema de vacunación para esta vacuna y el grupo "
                "de edad del paciente. Defínalo primero en Esquemas de Dosis"
            )

        # ---- qué dosis corresponde ----
        previas = self.servicio_esquema.dosis_previas(paciente_id, lote.vacuna_id)
        if previas and max(d.fecha for d in previas) > fecha_aplicacion:
            raise OperacionNoPermitidaError(
                "La fecha de aplicación es anterior a la última dosis del paciente"
            )

        proxima = determinar_proxima_dosis(regla, previas)
        if proxima is None:
            raise OperacionNoPermitidaError(
                "El paciente ya completó el esquema de esta vacuna y no requiere refuerzo"
            )
        if proxima.fecha_minima and fecha_aplicacion < proxima.fecha_minima:
            tipo = "el refuerzo" if proxima.es_refuerzo else f"la dosis {proxima.numero_dosis}"
            raise OperacionNoPermitidaError(
                f"Aún no corresponde aplicar {tipo}: puede aplicarse desde el {proxima.fecha_minima}"
            )

        if es_refuerzo is not None and es_refuerzo != proxima.es_refuerzo:
            esperado = "un refuerzo" if proxima.es_refuerzo else "una dosis de la serie primaria"
            raise OperacionNoPermitidaError(
                f"Según el esquema, al paciente le corresponde {esperado}"
            )
        if numero_dosis is not None and numero_dosis != proxima.numero_dosis:
            raise OperacionNoPermitidaError(
                f"Según el esquema, al paciente le corresponde la dosis número {proxima.numero_dosis}"
            )

        # ---- persistencia ----
        lote.descontar(1)
        registro = self.registro_repo.crear(
            RegistroVacunacion(
                paciente_id=paciente_id,
                campana_id=campana_id,
                punto_id=punto_id,
                lote_id=lote_id,
                vacuna_id=lote.vacuna_id,
                fecha_aplicacion=fecha_aplicacion,
                numero_dosis=proxima.numero_dosis,
                es_refuerzo=proxima.es_refuerzo,
            )
        )
        self.lote_repo.actualizar(lote)
        self.movimiento_repo.crear(
            MovimientoStock(
                lote_id=lote_id,
                tipo_movimiento="salida",
                cantidad=1,
                fecha_movimiento=datetime.now(),
                usuario_id=usuario_id,
                punto_id=punto_id,
                observacion=f"Dosis aplicada (registro de vacunación #{registro.id})",
            )
        )
        return registro
