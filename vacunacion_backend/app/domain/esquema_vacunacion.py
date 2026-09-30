"""Cálculo del estado de vacunación de un paciente para una vacuna.

Aquí vive la ÚNICA lógica que decide qué dosis toca aplicar (número de dosis,
si es refuerzo y desde qué fecha). La usan tanto el registro de dosis como
las consultas de dosis/refuerzos pendientes, para que nunca se contradigan.

La regla sale del esquema persistido (EsquemaVacunacion de
`entities.esquema_vacunacion`) que el administrador define por vacuna y
grupo de edad.
"""

from dataclasses import dataclass
from datetime import date, timedelta

from app.domain.entities.esquema_vacunacion import EsquemaVacunacion as ReglaEsquema


@dataclass(frozen=True)
class DosisPrevia:
    """Una dosis ya aplicada (en el sistema o como antecedente)."""

    fecha: date
    es_refuerzo: bool = False


@dataclass(frozen=True)
class ProximaDosis:
    numero_dosis: int
    es_refuerzo: bool
    fecha_minima: date | None  # None = puede aplicarse desde hoy


def sumar_meses(fecha: date, meses: int) -> date:
    indice = fecha.year * 12 + (fecha.month - 1) + meses
    anio, mes = divmod(indice, 12)
    mes += 1
    # ajusta el día si el mes destino es más corto (31 ene + 1 mes = 28/29 feb)
    for dia in (fecha.day, 30, 29, 28):
        try:
            return date(anio, mes, dia)
        except ValueError:
            continue
    raise ValueError("fecha inválida")  # pragma: no cover


def determinar_proxima_dosis(
    regla: ReglaEsquema, previas: list[DosisPrevia]
) -> ProximaDosis | None:
    """Qué dosis sigue según el esquema. None = esquema completo y sin
    refuerzos que aplicar."""
    ordenadas = sorted(previas, key=lambda d: d.fecha)
    serie = [d for d in ordenadas if not d.es_refuerzo]
    refuerzos = [d for d in ordenadas if d.es_refuerzo]
    ultima = ordenadas[-1].fecha if ordenadas else None

    if len(serie) < regla.cantidad_dosis:
        minima = (
            ultima + timedelta(days=regla.dias_entre_dosis) if ultima else None
        )
        return ProximaDosis(len(serie) + 1, False, minima)

    if not regla.requiere_refuerzo:
        return None

    minima = sumar_meses(ultima, regla.meses_refuerzo)
    return ProximaDosis(regla.cantidad_dosis + len(refuerzos) + 1, True, minima)


@dataclass
class EsquemaVacunacion:
    """Resumen calculado (no persistido) del estado de vacunación de un
    paciente para una vacuna: cuántas dosis de la serie lleva, cuántas le
    faltan y si tiene un refuerzo vencido/pendiente."""

    paciente_id: int
    vacuna_id: int
    dosis_aplicadas: int  # dosis de la serie primaria (sin contar refuerzos)
    dosis_requeridas: int
    tiene_refuerzo_pendiente: bool
    grupo_edad_id: int | None = None
    refuerzos_aplicados: int = 0
    proxima_dosis_numero: int | None = None
    proxima_dosis_es_refuerzo: bool | None = None
    fecha_minima_proxima_dosis: date | None = None

    @property
    def dosis_pendientes(self) -> int:
        return max(self.dosis_requeridas - self.dosis_aplicadas, 0)

    @property
    def esquema_completo(self) -> bool:
        return self.dosis_pendientes == 0 and not self.tiene_refuerzo_pendiente

    @classmethod
    def calcular(
        cls,
        paciente_id: int,
        vacuna_id: int,
        regla: ReglaEsquema,
        previas: list[DosisPrevia],
        hoy: date,
    ) -> "EsquemaVacunacion":
        serie = [d for d in previas if not d.es_refuerzo]
        refuerzos = [d for d in previas if d.es_refuerzo]
        proxima = determinar_proxima_dosis(regla, previas)

        refuerzo_pendiente = bool(
            proxima
            and proxima.es_refuerzo
            and proxima.fecha_minima is not None
            and hoy >= proxima.fecha_minima
        )
        return cls(
            paciente_id=paciente_id,
            vacuna_id=vacuna_id,
            dosis_aplicadas=len(serie),
            dosis_requeridas=regla.cantidad_dosis,
            tiene_refuerzo_pendiente=refuerzo_pendiente,
            grupo_edad_id=regla.grupo_edad_id,
            refuerzos_aplicados=len(refuerzos),
            proxima_dosis_numero=proxima.numero_dosis if proxima else None,
            proxima_dosis_es_refuerzo=proxima.es_refuerzo if proxima else None,
            fecha_minima_proxima_dosis=proxima.fecha_minima if proxima else None,
        )
