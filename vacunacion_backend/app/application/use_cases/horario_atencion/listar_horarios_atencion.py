from app.domain.entities.horario_atencion import HorarioAtencion
from app.domain.repositories.horario_atencion_repository import (
    HorarioAtencionRepository,
)


class ListarHorariosAtencion:
    def __init__(self, repo: HorarioAtencionRepository):
        self.repo = repo

    def ejecutar(self, punto_id: int | None = None) -> list[HorarioAtencion]:
        if punto_id is not None:
            return self.repo.listar_por_punto(punto_id)
        return self.repo.listar()
