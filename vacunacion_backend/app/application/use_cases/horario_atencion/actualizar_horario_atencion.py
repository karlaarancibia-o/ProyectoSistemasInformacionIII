from datetime import time

from app.domain.entities.horario_atencion import HorarioAtencion
from app.domain.exceptions import NoEncontradoError
from app.domain.repositories.horario_atencion_repository import (
    HorarioAtencionRepository,
)


class ActualizarHorarioAtencion:
    """Complementa el evento 5 (diagrama nivel 2: 'Actualizar horario'):
    el administrador corrige el día u horario de atención ya definido para
    un punto de vacunación."""

    def __init__(self, repo: HorarioAtencionRepository):
        self.repo = repo

    def ejecutar(
        self,
        horario_id: int,
        dia_semana: int,
        hora_apertura: time,
        hora_cierre: time,
    ) -> HorarioAtencion:
        horario = self.repo.obtener_por_id(horario_id)
        if not horario:
            raise NoEncontradoError("Horario de atención no encontrado")

        horario.dia_semana = dia_semana
        horario.hora_apertura = hora_apertura
        horario.hora_cierre = hora_cierre
        HorarioAtencion(**vars(horario))  # revalida invariantes del dominio

        return self.repo.actualizar(horario)
