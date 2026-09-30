"""Entidad persistida: regla de vacunación de una vacuna para un grupo de
edad (cuántas dosis, cada cuánto y si requiere refuerzo).

No confundir con `app.domain.esquema_vacunacion.EsquemaVacunacion`, que es
un resumen calculado (no persistido) del estado de vacunación de un
paciente, usado por los casos de uso de dosis/refuerzos pendientes.
"""

from dataclasses import dataclass

from app.domain.exceptions import DatosInvalidosError


@dataclass
class EsquemaVacunacion:
    vacuna_id: int
    grupo_edad_id: int
    cantidad_dosis: int
    dias_entre_dosis: int
    requiere_refuerzo: bool = False
    meses_refuerzo: int | None = None
    id: int | None = None

    def __post_init__(self):
        if self.cantidad_dosis <= 0:
            raise DatosInvalidosError("La cantidad de dosis debe ser positiva")
        if self.dias_entre_dosis < 0:
            raise DatosInvalidosError("Los días entre dosis no pueden ser negativos")
        if self.requiere_refuerzo and not self.meses_refuerzo:
            raise DatosInvalidosError(
                "Si el esquema requiere refuerzo, debe indicarse cada cuántos meses"
            )

    def validar_coherencia(self) -> None:
        """Reglas de negocio que se exigen al CREAR o EDITAR un esquema.

        No están en __post_init__ para no romper la lectura de esquemas
        antiguos ya guardados en la base de datos.

        - cantidad_dosis: dosis de la serie primaria.
        - dias_entre_dosis: intervalo mínimo entre dosis de la serie primaria
          (no aplica si la serie es de una sola dosis).
        - refuerzo: dosis adicional que se aplica cada `meses_refuerzo` meses
          después de completar la serie (o del refuerzo anterior).
        """
        if self.cantidad_dosis == 1 and self.dias_entre_dosis != 0:
            raise DatosInvalidosError(
                "Si el esquema es de una sola dosis, los días entre dosis deben ser 0"
            )
        if self.cantidad_dosis > 1 and self.dias_entre_dosis <= 0:
            raise DatosInvalidosError(
                "Si el esquema tiene más de una dosis, indique los días entre dosis (mayor a 0)"
            )
        if not self.requiere_refuerzo and self.meses_refuerzo is not None:
            raise DatosInvalidosError(
                "No puede indicar meses de refuerzo si el esquema no requiere refuerzo"
            )
