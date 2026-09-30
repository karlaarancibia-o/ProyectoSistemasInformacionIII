from datetime import time

from app.domain.entities.horario_atencion import HorarioAtencion
from app.domain.exceptions import NoEncontradoError
from app.domain.repositories.horario_atencion_repository import (
    HorarioAtencionRepository,
)
from app.domain.repositories.punto_vacunacion_repository import (
    PuntoVacunacionRepository,
)


class DefinirHorarioAtencion:
    """Evento 5: El administrador registra el horario de atención de un
    punto."""

    def __init__(
        self, repo: HorarioAtencionRepository, punto_repo: PuntoVacunacionRepository
    ):
        self.repo = repo
        self.punto_repo = punto_repo

    def ejecutar(
        self, punto_id: int, dia_semana: int, hora_apertura: time, hora_cierre: time
    ) -> HorarioAtencion:
        if not self.punto_repo.obtener_por_id(punto_id):
            raise NoEncontradoError("Punto de vacunación no encontrado")

        horario = HorarioAtencion(
            punto_id=punto_id,
            dia_semana=dia_semana,
            hora_apertura=hora_apertura,
            hora_cierre=hora_cierre,
        )
        return self.repo.crear(horario)
