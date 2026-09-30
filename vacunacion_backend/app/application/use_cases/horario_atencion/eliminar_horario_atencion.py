from app.application.use_cases.horario_atencion.obtener_horario_atencion import (
    ObtenerHorarioAtencion,
)
from app.domain.repositories.horario_atencion_repository import (
    HorarioAtencionRepository,
)


class EliminarHorarioAtencion:
    def __init__(self, repo: HorarioAtencionRepository):
        self.repo = repo

    def ejecutar(self, horario_id: int) -> None:
        ObtenerHorarioAtencion(self.repo).ejecutar(horario_id)
        self.repo.eliminar(horario_id)
