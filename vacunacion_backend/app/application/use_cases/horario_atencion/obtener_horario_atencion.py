from app.domain.entities.horario_atencion import HorarioAtencion
from app.domain.exceptions import NoEncontradoError
from app.domain.repositories.horario_atencion_repository import (
    HorarioAtencionRepository,
)


class ObtenerHorarioAtencion:
    def __init__(self, repo: HorarioAtencionRepository):
        self.repo = repo

    def ejecutar(self, horario_id: int) -> HorarioAtencion:
        horario = self.repo.obtener_por_id(horario_id)
        if not horario:
            raise NoEncontradoError("Horario de atención no encontrado")
        return horario
